from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanApplicationSerializer
from users.models import UserProfile
from .utils import generate_emi_schedule

LOAN_LIMITS = {
    'Car': 750000,
    'Home': 8500000,
    'Education': 5000000,
    'Personal': 1000000
}

# Class for ApplyLoanAPIView which will display loan id and the due dates
class ApplyLoanAPIView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get("unique_user_id")

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({"error": "User not found."}, status=400)

        if user.credit_score is None or user.credit_score < 200:
            return Response({"error": "Credit score not sufficient or not calculated yet."}, status=400)

        if user.annual_income < 150000:
            return Response({"error": "Income below eligible threshold."}, status=400)

        loan_type = data.get("loan_type")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        term_period = int(data.get("term_period"))
        disbursement_date = data.get("disbursement_date")

        if loan_type not in LOAN_LIMITS:
            return Response({"error": "Unsupported loan type."}, status=400)

        if loan_amount > LOAN_LIMITS[loan_type]:
            return Response({"error": "Loan amount exceeds allowed limit for this type."}, status=400)

        if interest_rate < 14:
            return Response({"error": "Interest rate below 14%."}, status=400)

        emi_schedule, error = generate_emi_schedule(
            principal=loan_amount,
            rate=interest_rate,
            months=term_period,
            start_date=disbursement_date,
            monthly_income=user.annual_income
        )

        if error:
            return Response({"error": error}, status=400)

        loan = Loan.objects.create(
            user=user,
            loan_type=loan_type,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            term_period=term_period,
            disbursement_date=disbursement_date,
            emi_schedule=emi_schedule
        )

        return Response({
            "error": None,
            "loan_id": loan.id,
            "due_dates": emi_schedule
        }, status=200)
