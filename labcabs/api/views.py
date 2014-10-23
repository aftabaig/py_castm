
import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import list_route

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

consignment_list = ConsignmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
consignment_detail = ConsignmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
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