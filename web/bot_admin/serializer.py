from rest_framework import serializers


class AmountSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()


class MetadataSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    tariff_id = serializers.IntegerField()
    # если нужны ещё поля:
    cms_name = serializers.CharField(required=False)


class PaymentObjectSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()
    amount = AmountSerializer()
    metadata = MetadataSerializer()


class YooKassaWebhookSerializer(serializers.Serializer):
    type = serializers.CharField()
    event = serializers.CharField()
    object = PaymentObjectSerializer()
