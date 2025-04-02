import uuid
from django.db import models

# Class for UserProfile containting aadhar_id, name, email and annual income 
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aadhar_id = models.CharField(max_length=36, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    annual_income = models.PositiveIntegerField()
    credit_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# Class for the transactions where type can be DEBIT or CREDIt
class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('DEBIT', 'Debit'), ('CREDIT', 'Credit')])
