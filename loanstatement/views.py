

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from loanapp.models import Loan, Payment  # Reuse models from loanapp
from datetime import datetime

class GetLoanStatementAPIView(APIView):
    def post(self, request):
        loan_id = request.data.get("loan_id")

        try:
            loan = Loan.objects.get(id=loan_id)
        except Loan.DoesNotExist:
            return Response({"error": "Loan does not exist."}, status=400)

        if loan.is_closed:
            return Response({"error": "Loan is already closed."}, status=400)

        emi_schedule = loan.emi_schedule
        payments = Payment.objects.filter(loan=loan).order_by('date')

        paid_list = list(payments)
        emi_list = list(emi_schedule)

        past_transactions = []
        upcoming_transactions = []

        monthly_rate = loan.interest_rate / 12 / 100
        principal_remaining = float(loan.loan_amount)
        total_paid_principal = 0

        # Process past payments
        for i, emi in enumerate(emi_list):
            due_date = emi['date']
            due_amount = float(emi['amount_due'])

            if i < len(paid_list):  # If there's a payment for this installment
                payment = paid_list[i]
                interest = round(principal_remaining * monthly_rate, 2)
                principal = round(payment.amount_paid - interest, 2)
                principal_remaining = max(0, principal_remaining - principal)
                total_paid_principal += principal

                past_transactions.append({
                    "date": due_date,
                    "principal": principal,
                    "interest": interest,
                    "amount_paid": float(payment.amount_paid)
                })
            else:  # Upcoming transaction
                upcoming_transactions.append({
                    "date": due_date,
                    "amount_due": due_amount
                })

        # Add current balance and tenure left
        current_balance = round(principal_remaining, 2)
        tenure_left = len(emi_list) - len(paid_list)

        return Response({
            "error": None,
            "current_balance": current_balance,
            "tenure_left": tenure_left,
            "past_transactions": past_transactions,
            "upcoming_transactions": upcoming_transactions
            
        }, status=200)
