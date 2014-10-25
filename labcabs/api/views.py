
import logging
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import list_route
from rest_framework.decorators import detail_route
from rest_framework.decorators import action

# serializers
from serializers import EntitySerializer
from serializers import EntityTypeSerializer
from serializers import ConsignmentSerializer
from serializers import SupplySerializer
from serializers import SearchSerializer

# models
from models import Entity
from models import Supply
from models import Consignment
from models import ConsignmentSupply
from models import Search

logger = logging.getLogger(__name__)


class EntityMixin(object):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class EntityViewSet(EntityMixin, viewsets.ModelViewSet):

    @list_route()
    def entity_types(self, request):
        unique_types = Entity.objects.order_by('type').distinct('type')
        logger.debug(unique_types)
        serializer = EntityTypeSerializer(unique_types, many=True)
        return Response(serializer.data)


entity_list = EntityViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
entity_detail = EntityViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

entity_router = DefaultRouter()
entity_router.register(r'entities', EntityViewSet)


class ConsignmentMixin(object):
    queryset = Consignment.objects.all()
    serializer_class = ConsignmentSerializer


class ConsignmentViewSet(ConsignmentMixin, viewsets.ModelViewSet):

    @list_route(methods=['post', ])
    def send(self, request):

        consignment_ids = request.DATA.get("consignment_ids")
        entity = request.DATA.get("entity")
        subject = request.DATA.get("subject")
        fields = request.DATA.get("fields")

        html = ""
        html += "<table style='width:100%;border-style:solid;border-width:1px'>"
        html += "\t<tr>"
        html += "\t\t<td>"
        html += "\t\t\t<strong>#"
        html += "\t\t</td>"

        for f in fields:
            if f.get("selected"):
                html += "\t\t<td>"
                html += "\t\t\t<strong>%s</strong>" % (f.get("title"), )
                html += "\t\t</td>"
        html += "\t</tr>"

        for c_id in consignment_ids:
            logger.debug(c_id)
            c = Consignment.objects.get(pk=c_id)
            html += "\t<tr>"
            html += "\t\t<td>%s</td>" % (c.id, )
            for f in fields:
                if f.get("selected"):
                    html += "\t\t<td>"
                    name = f.get("name")
                    if name == 'consignor':
                        html += "%s" % (c.consignor.name, )
                    elif name == 'consignee':
                        html += "%s" % (c.consignee.name, )
                    elif name == 'originator':
                        html += "%s" % (c.originator.name, )
                    elif name == 'account':
                        html += "%s" % (c.account.description, )
                    elif name == 'pickup_address':
                        html += "%s %s %s %s %s %s %s" % (c.pickup_tenancy, c.pickup_street_num, c.pickup_street, c.pickup_town, c.pickup_postcode, c.pickup_state, c.pickup_country, )
                    elif name == 'delivery_address':
                        html += "%s %s %s %s %s %s %s" % (c.delivery_tenancy, c.delivery_street_num, c.delivery_street, c.delivery_town, c.delivery_postcode, c.delivery_state, c.delivery_country, )
                    elif name == 'mode':
                        html += "%s" % (c.mode, )
                    elif name == 'status':
                        html += "%s" % (c.status, )
                    elif name == 'pickup_date':
                        html += "%s" % (c.pickupDate, )
                    elif name == 'eta_date':
                        html += "%s" % (c.eta_date, )
                    elif name == 'notes':
                        html += "%s" % (c.notes, )
                    elif name == 'customer_reference':
                        html += "%s" % (c.customer_reference, )
                    html += "\t\t</td>"
            html += "\t</tr>"


        html += "</table>"

        send_mail(subject, 'Message', 'info@labcabs.com', [entity.get("email"), ], html_message=html)
        return Response(None)

    def post_save(self, obj, created=False):
        if not created:
            ConsignmentSupply.objects.filter(consignment_id=obj.id).delete()

        supplies = self.request.DATA.get("supplies")
        if supplies is not None:
            for s in supplies:
                amount = s.get("amount")
                supply_dict = s.get("supply")
                supply_id = supply_dict.get("id")
                supply = Supply.objects.get(id=supply_id)
                ConsignmentSupply.objects.get_or_create(consignment=obj, supply=supply, amount=amount)

consignment_email = ConsignmentViewSet.as_view({
    'post': 'send_as_email',
})
consignments_send = ConsignmentViewSet.as_view({
    'post': 'send'
})
consignment_list = ConsignmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
consignment_detail = ConsignmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})


consignment_router = DefaultRouter()
consignment_router.register(r'consignments', ConsignmentViewSet)


class SupplyMixin(object):
    queryset = Supply.objects.all()
    serializer_class = SupplySerializer


class SupplyViewSet(SupplyMixin, viewsets.ModelViewSet):
    pass

supply_list = SupplyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
supply_detail = SupplyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

supply_router = DefaultRouter()
supply_router.register(r'supplies', SupplyViewSet)


class SearchMixin(object):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer


class SearchViewSet(SearchMixin, viewsets.ModelViewSet):
    pass

search_list = SearchViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
search_detail = SearchViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

search_router = DefaultRouter()
search_router.register(r'searches', SearchViewSet)