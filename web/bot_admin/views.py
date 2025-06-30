from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LavaCallbackSerializer
import logging

logger = logging.getLogger(__name__)

class LavaCallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = LavaCallbackSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data

            pay_status = validated_data['status']
            order_id = validated_data['order_id']
            custom_fields = validated_data.get('custom_fields', "")
            amount = validated_data['amount']

            logger.info(f"Lava callback valid: {validated_data}")

            # TODO: твоя обработка оплаты:
            # Например, найти заказ по order_id, проверить сумму и статус, записать оплату в базу и т.д.

            return Response({'ok': True}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"Lava callback invalid: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
