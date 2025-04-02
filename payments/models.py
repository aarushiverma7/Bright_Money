from django.db import models
from loanapp.models import Loan


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
     # Date field to store the date when the payment was made
    date = models.DateField()
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payment of ₹{self.amount_paid} on {self.date} for Loan {self.loan.id}"
