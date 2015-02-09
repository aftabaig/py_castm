from rest_framework import serializers


class PlainPaymentPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField(required=False, read_only=True)
    plan_title = serializers.CharField(required=False, read_only=True)
    plan_charges = serializers.FloatField(required=False, read_only=True)
    can_upgrade = serializers.CharField(required=False, read_only=True)
    can_downgrade = serializers.CharField(required=False, read_only=True)