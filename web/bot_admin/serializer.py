from rest_framework import serializers


class LavaCallbackSerializer(serializers.Serializer):
    status = serializers.CharField()
    order_id = serializers.CharField()
    custom_fields = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.IntegerField()
    # Добавь другие нужные поля по структуре callback-а
