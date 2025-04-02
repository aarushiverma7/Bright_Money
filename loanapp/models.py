import uuid
from django.db import models
from users.models import UserProfile

LOAN_TYPE_CHOICES = [
    ('Car', 'Car'),
    ('Home', 'Home'),
    ('Education', 'Education'),
    ('Personal', 'Personal'),
]

# Class for Loans where types can be Car, Home, Education and Personal
class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.FloatField()
    term_period = models.PositiveIntegerField(help_text="Months")
    disbursement_date = models.DateField()
    emi_schedule = models.JSONField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.loan_type} loan for {self.user.name}"

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.loan.id} - {self.amount} on {self.date}"
