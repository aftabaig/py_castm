
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

# serializers
from serializers import EntitySerializer
from serializers import ConsignmentSerializer

# models
from models import Entity
from models import Consignment


class EntityMixin(object):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class EntityViewSet(EntityMixin, viewsets.ModelViewSet):
    pass


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
    pass


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
