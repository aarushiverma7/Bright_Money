from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math

def generate_emi_schedule(principal, rate, months, start_date, monthly_income):
    # Convert annual interest to monthly
    r = rate / 12 / 100
    emi = (principal * r * (1 + r)**months) / ((1 + r)**months - 1)
    emi = round(emi, 2)

    # Cap EMI to 60% of monthly income
    if emi > 0.6 * (monthly_income / 12):
        return None, "EMI exceeds 60% of monthly income"

    # Total interest check
    total_payment = emi * months
    total_interest = total_payment - principal
    if total_interest <= 10000:
        return None, "Total interest earned is not sufficient"

    schedule = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d") + relativedelta(months=1)

    for i in range(months):
        due_date = current_date + relativedelta(months=i)
        schedule.append({
            "date": due_date.strftime("%Y-%m-%d"),
            "amount_due": round(emi if i < months - 1 else total_payment - emi * (months - 1), 2)
        })

    return schedule, None
