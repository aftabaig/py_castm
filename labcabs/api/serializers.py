from rest_framework import serializers

# models
from models import Entity
from models import EntityRelationship
from models import Consignment
from models import ConsignmentItem
from models import ConsignmentCharge


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRelationship


class EntitySerializer(serializers.ModelSerializer):
    entity_relationships = RelationshipSerializer(many=True, allow_add_remove=True, required=False)

    class Meta:
        model = Entity
        fields = ('id',
                  'name',
                  'type',
                  'tenancy',
                  'street_num',
                  'street',
                  'town',
                  'postcode',
                  'state',
                  'country',
                  'entity_relationships')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentItem
        fields = ('id',
                  'description',
                  'width',
                  'length',
                  'height',
                  'weight',
                  'temp')


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentCharge
        fields = ('id',
                  'description',
                  'cost',
                  'quantity')


class ConsignmentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, allow_add_remove=True, required=False)
    charges = ChargeSerializer(many=True, allow_add_remove=True, required=False)

    class Meta:
        model = Consignment
        fields = ('id',
                  'consignor',
                  'consignee',
                  'account',
                  'mode',
                  'status',
                  'pickupDate',
                  'notes',
                  'items',
                  'charges')

