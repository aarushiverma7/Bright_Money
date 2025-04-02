from rest_framework import serializers
from .models import Loan

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ['emi_schedule', 'is_closed']
