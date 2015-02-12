import logging
import stripe
import json

from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.models import User

from models import PaymentPlan, UserSubscription, StripeEvent
from organizations.models import Organization, OrganizationMember
from notifications.views import create_notification

from serializers import PlainPaymentPlanSerializer

from um.views import error_as_text
from um.permissions import IsTalentOrCasting

logger = logging.getLogger(__name__)

CHARGE_SUCCESS = "charge.succeeded"
CHARGE_FAIL = "charge.failed"

stripe.api_key = settings.STRIPE['secret_key']


def __get_user_plans__(user):
    plain_user_plans = []
    user_plans = PaymentPlan.user_plans(user)
    for plan in user_plans:
        plain_user_plans.append(plan.plain())
    return plain_user_plans


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting])
def plans(request):
    user = request.user
    user_plans = __get_user_plans__(user)
    serializer = PlainPaymentPlanSerializer(user_plans, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def subscribe(request):

    user = request.user
    user_organization = None
    user_subscription = UserSubscription.user_subscription(user)

    if user.my_user.type == 'C':
        user_organization = OrganizationMember.user_organization(user)
        if not user_organization:
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "You must be an approved member of an organization to be able to subscribe for a plan"
            }, status=HTTP_400_BAD_REQUEST)
        if user_subscription and (user_subscription.status == 'AS' or user_subscription.status == 'PN'):
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "Your organization already have an active subscription"
            }, status=HTTP_400_BAD_REQUEST)
    else:
        if user_subscription and (user_subscription.status == 'AS' or user_subscription.status == 'PN'):
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "You already have an active/pending subscription"
            })

    plan_id = request.DATA.get("plan_id")
    stripe_token = request.DATA.get("stripeToken")
    plan = PaymentPlan.objects.filter(id=plan_id).first()
    if plan:

        subscription = user_subscription
        stripe_customer = None

        if stripe_token is None:
            if subscription is None:
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Token not specified"
                }, status=HTTP_400_BAD_REQUEST)

        if subscription is None:
            subscription = UserSubscription(user=user, organization=user_organization, plan=plan)
            stripe_customer = stripe.Customer.create(
                description=user.email,
                card=stripe_token
            )
            if stripe_customer:
                subscription.stripe_customer_id = stripe_customer.id
            else:
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Error creating customer"
                }, status=HTTP_400_BAD_REQUEST)
        else:
            stripe_customer = stripe.Customer.retrieve(subscription.stripe_customer_id)
            if stripe_customer is None:
                return Response({
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Error retrieving customer"
                }, status=HTTP_400_BAD_REQUEST)

        stripe_subscription = stripe_customer.subscriptions.create(
            plan=plan.name
        )
        if stripe_subscription:
            subscription.stripe_subscription_id = stripe_subscription.id
            subscription.status = "AS"
            subscription.save()
            return Response({
                "status": HTTP_200_OK,
                "message": "OK"
            })
        else:
            return Response({
                "status": HTTP_400_BAD_REQUEST,
                "message": "Error creating subscription"
            }, status=HTTP_400_BAD_REQUEST)

    return Response({
        "status": HTTP_404_NOT_FOUND,
        "message": "Plan not found"
    }, status=HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes([IsTalentOrCasting, ])
def un_subscribe(request):

    user = request.user
    subscription = UserSubscription.user_subscription(user)

    if subscription is None:
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "You don't have any subscription"
        })



    if subscription.status == "AS" or subscription.status == "PN":

        stripe_customer = stripe.Customer.retrieve(subscription.stripe_customer_id)
        if stripe_customer:
            stripe_subscription = stripe_customer.subscriptions.retrieve(subscription.stripe_subscription_id)
            if stripe_subscription:
                stripe_subscription.delete(at_period_end=True)
                subscription.status = "US"
                subscription.save()
                return Response({
                    "status": HTTP_200_OK,
                    "message": "OK"
                })
            return Response({
                "status": HTTP_404_NOT_FOUND,
                "message": "Error receiving stripe subscription"
            }, status=HTTP_404_NOT_FOUND)
        return Response({
            "status": HTTP_404_NOT_FOUND,
            "message": "Error receiving stripe customer"
        }, status=HTTP_404_NOT_FOUND)

    return Response({
        "status": HTTP_400_BAD_REQUEST,
        "message": "You are already un-subscribed"
    }, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsTalentOrCasting, ])
def subscription_status(request):
    user = request.user
    if user.my_user.type == 'T':
        subscription = UserSubscription.user_subscription(user)
    else:
        subscription = UserSubscription.user_subscription(user)

    if subscription is None:
        return Response({
            "status": HTTP_200_OK,
            "data": {
                "status": "NS",
                "plan": None
            }
        })

    return Response({
        "status": HTTP_200_OK,
        "data": {
            "status": subscription.status,
            "plan": {
                "plan_id": subscription.plan.id,
                "plan_title": subscription.plan.title,
                "plan_charges": subscription.plan.charges,
                "can_upgrade": subscription.plan.can_upgrade,
                "can_downgrade": subscription.plan.can_downgrade
            }
        }
    })


@api_view(['POST', ])
def event_handler(request):

    stripe_event_json = json.loads(request.body)
    stripe_event_id = stripe_event_json["id"]
    stripe_event_type = stripe_event_json["type"]

    logger.debug("stripe_event")
    logger.debug(stripe_event_json)

    logger.debug("event_id")
    logger.debug(stripe_event_id)

    logger.debug("event_type")
    logger.debug(stripe_event_type)

    stripe_event = StripeEvent.objects.filter(stripe_event_id=stripe_event_id).first()
    if stripe_event is None:
        stripe_event = StripeEvent(stripe_event_id=stripe_event_id, stripe_event_type=stripe_event_type)
        if stripe_event_type == CHARGE_SUCCESS or stripe_event_type == CHARGE_FAIL:
            stripe_data = stripe_event_json["data"]
            stripe_charge = stripe_data["object"]
            stripe_card = stripe_charge["card"]
            stripe_customer_id = stripe_card["customer"]
            subscription = UserSubscription.objects.filter(stripe_customer_id=stripe_customer_id).first()
            if subscription:
                if stripe_event_type == CHARGE_SUCCESS:
                    subscription.status = "AS"
                else:
                    subscription.status = "FS"
                subscription.save()
                stripe_event.user = subscription.user
        stripe_event.save()

    return Response(status=HTTP_200_OK)
