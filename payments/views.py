from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from loanapp.models import Loan
from .serializers import PaymentSerializer
from datetime import datetime

class MakePaymentAPIView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            loan_id = serializer.validated_data['loan_id']
            amount_paid = serializer.validated_data['amount']

            try:
                loan = Loan.objects.get(id=loan_id)
            except Loan.DoesNotExist:
                return Response({"error": "Loan not found."}, status=400)

            emi_schedule = loan.emi_schedule
            payments = Payment.objects.filter(loan=loan).order_by('date')
            paid_dates = {p.date.strftime("%Y-%m-%d") for p in payments}

            # Find next unpaid EMI
            next_emi = None
            for emi in emi_schedule:
                if emi['date'] not in paid_dates:
                    next_emi = emi
                    break

            if not next_emi:
                return Response({"error": "All EMIs are already paid."}, status=400)

            # Check if previous EMIs are all paid
            due_index = emi_schedule.index(next_emi)
            for prev in emi_schedule[:due_index]:
                if prev['date'] not in paid_dates:
                    return Response({"error": "Previous EMIs are unpaid."}, status=400)

            if next_emi['date'] in paid_dates:
                return Response({"error": "EMI already paid for this date."}, status=400)

            # Save payment
            Payment.objects.create(
                loan=loan,
                date=datetime.strptime(next_emi['date'], "%Y-%m-%d"),
                amount_paid=amount_paid
            )

            # If overpaid or underpaid: adjust future EMIs
            if amount_paid != next_emi['amount_due']:
                pending = emi_schedule[due_index + 1:]
                new_balance = sum([emi['amount_due'] for emi in emi_schedule[due_index:]]) - float(amount_paid)

                if new_balance <= 0:
                    emi_schedule = emi_schedule[:due_index + 1]
                else:
                    monthly_count = len(pending)
                    if monthly_count > 0:
                        new_emi = round(new_balance / monthly_count, 2)
                        for i, emi in enumerate(pending):
                            emi_schedule[due_index + 1 + i]['amount_due'] = new_emi
                        emi_schedule[due_index]['amount_due'] = float(amount_paid)

                loan.emi_schedule = emi_schedule
                loan.save()

            return Response({"error": None}, status=200)

        return Response({"error": serializer.errors}, status=400)
