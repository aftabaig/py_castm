from rest_framework import serializers

# models
from models import Supply
from models import Entity
from models import EntityRelationship
from models import EntityAccount
from models import Consignment
from models import ConsignmentItem
from models import ConsignmentCharge
from models import ConsignmentSupply
from models import Search
from models import SearchField
from models import SearchCriterion


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRelationship


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityAccount
        fields = ('id',
                  'description')


class EntitySerializer(serializers.ModelSerializer):
    relationships = RelationshipSerializer(many=True, allow_add_remove=True, required=False)
    accounts = AccountSerializer(many=True, allow_add_remove=True, required=False)

    class Meta:
        model = Entity
        fields = ('id',
                  'name',
                  'type',
                  'email',
                  'tenancy',
                  'street_num',
                  'street',
                  'town',
                  'postcode',
                  'state',
                  'country',
                  'relationships',
                  'accounts')


class EntityTypeSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=255)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentItem
        fields = ('id',
                  'description',
                  'width',
                  'length',
                  'height',
                  'dead_weight',
                  'temp')


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsignmentCharge
        fields = ('id',
                  'description',
                  'cost',
                  'quantity')


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = ('id',
                  'description')


class ConsignmentSupplySerializer(serializers.ModelSerializer):
    supply = SupplySerializer()

    class Meta:
        model = ConsignmentSupply
        fields = ('supply',
                  'amount')


class ConsignmentSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, allow_add_remove=True, required=False)
    charges = ChargeSerializer(many=True, allow_add_remove=True, required=False)
    supplies = ConsignmentSupplySerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Consignment
        fields = ('id',
                  'consignor',
                  'consignee',
                  'originator',
                  'account',
                  'pickup_tenancy',
                  'pickup_street_num',
                  'pickup_street',
                  'pickup_town',
                  'pickup_postcode',
                  'pickup_state',
                  'pickup_country',
                  'delivery_tenancy',
                  'delivery_street_num',
                  'delivery_street',
                  'delivery_town',
                  'delivery_postcode',
                  'delivery_state',
                  'delivery_country',
                  'mode',
                  'status',
                  'pickupDate',
                  'eta_date',
                  'notes',
                  'customer_reference',
                  'items',
                  'charges',
                  'supplies')


class SearchFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchField
        fields = ('id',
                  'name',
                  'title',
                  'selected',)


class SearchCriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchCriterion
        fields = ('id',
                  'criterion',
                  'criterion_value')


class SearchSerializer(serializers.ModelSerializer):
    fields = SearchFieldSerializer(many=True, allow_add_remove=True, required=False)
    criteria = SearchCriterionSerializer(many=True, allow_add_remove=True, required=False)

    class Meta:
        model = Search
        fields = ('id',
                  'name',
                  'fields',
                  'criteria',)
