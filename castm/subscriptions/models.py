from django.db import models
from django.contrib.auth.models import User

from organizations.models import Organization


class PaymentPlan(models.Model):

    user_type_choices = (
        ('T', 'Talent'),
        ('C', 'Casting'),
    )

    plan_type = models.CharField("Plan Type", max_length=1, choices=user_type_choices, blank=False)
    name = models.CharField("Plan Name", max_length=64, blank=False)
    title = models.CharField("Plan Title", max_length=128, blank=False)
    charges = models.FloatField("Charges /Month", blank=False)
    can_upgrade = models.BooleanField("Can Upgrade?", blank=False, default=False)
    can_downgrade = models.BooleanField("Can Downgrade?", blank=False, default=False)

    def plain(self):
        return PlainPaymentPlan(
            plan_id=self.id,
            plan_title=self.title,
            plan_charges=self.charges,
            can_upgrade=self.can_upgrade,
            can_downgrade=self.can_downgrade
        )


    @staticmethod
    def user_plans(user):
        q = models.Q(user_type=user.my_user.type)
        return PaymentPlan.objects.filter(q)


class UserSubscription(models.Model):

    status_type_choices = (
        ('AS', 'Active Subscription'),
        ('US', 'Un-subscribed'),
        ('FS', 'Failed Subscription'),
        ('PN', 'Pending'),
    )

    user = models.OneToOneField(User, related_name="subscription")
    organization = models.OneToOneField(Organization, related_name="organization_subscription")
    plan = models.ForeignKey(PaymentPlan)
    stripe_customer_id = models.CharField("Customer #", max_length=128, blank=False)
    stripe_subscription_id = models.CharField("Subscription #", max_length=128, blank=False)
    status = models.CharField("Payment Status", max_length=2, choices=status_type_choices, blank=False)


class StripeEvent(models.Model):
    user = models.ForeignKey(User, related_name="stripe_events", null=True)
    stripe_event_id = models.CharField("Stripe Event Id", max_length=64, blank=False)
    stripe_event_type = models.CharField("Event Type", max_length=64, blank=False)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)


class PlainPaymentPlan(object):
    def __init__(self, plan_id=None, plan_title=None, plan_charges=None, can_upgrade=None, can_downgrade=None):
        self.plan_id = plan_id
        self.plan_title = plan_title
        self.plan_charges = plan_charges
        self.can_upgrade = can_upgrade
        self.can_downgrade = can_downgrade

