from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    loan_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
