import os
import pandas as pd
from celery import shared_task
from .models import UserProfile

# Function for calculation of the credit score based on the balance 
@shared_task
def calculate_credit_score_task(aadhar_id):
    try:
        user = UserProfile.objects.get(aadhar_id=aadhar_id)

        csv_path = os.path.join(os.path.dirname(__file__), '..', 'Transactions.csv')
        csv_path = os.path.abspath(csv_path)

        df = pd.read_csv(csv_path)

        df = df[df['user'] == aadhar_id]

        if df.empty:
            print(f"No transactions found for AADHAR: {aadhar_id}")
            return
        balance = 0
        for _, row in df.iterrows():
            if row['transaction_type'] == 'CREDIT':
                balance += row['amount']
            else:
                balance -= row['amount']

        if balance >= 1_000_000:
            score = 900
        elif balance <= 100_000:
            score = 300
        else:
            score = 300 + int((balance - 100000) / 15000) * 10
            score = min(score, 900)

        user.credit_score = score
        user.save()
        print(f" Credit score for {user.name} updated to {score}")

    except Exception as e:
        print(f" Error in calculate_credit_score_task: {str(e)}")
