# Credimate - Loan Management System

Credimate is a Django-based web application designed to help loan service companies efficiently manage loan operations such as user registration, credit score evaluation, loan applications, EMI scheduling, and payment tracking.

## Features

- User registration with Aadhar ID and annual income
- Asynchronous credit score calculation using Celery
- Loan application with eligibility checks and EMI scheduling
- EMI payments and dynamic rescheduling on over/under payment
- Loan statement generation with principal and interest breakdown
- RESTful API endpoints using Django REST Framework

## Technologies Used

- Django 5
- Celery with Redis
- SQLite (default, can be replaced)
- Python 3
- Pandas (for CSV parsing)
- Django REST Framework

## Project Structure

```
credimate/
├── credimate/          # Main settings and configurations
│   ├── __init__.py     # Initializes Celery
│   ├── celery.py       # Celery app configuration
│   ├── settings.py     # Django settings
│   ├── urls.py         # Root URL configuration
├── users/              # User registration and credit scoring
├── loanapp/            # Loan application and EMI logic
├── payments/           # EMI payment processing
├── loanstatement/      # Loan statement generation
├── Transactions.csv    # Sample transaction data for scoring
├── db.sqlite3          # SQLite database
```

## Setup Instructions

Follow these steps to set up and run the Credimate Loan Management System on your local development environment.

### 1. Clone the Repository

```bash
git clone https://github.com/aarushiverma7/Bright--money
cd credimate
```

### 2. Create a Virtual Environment python -m venv venv

venv\Scripts\activate

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Redis for Celery

Make sure Redis is installed and running. You can start Redis in docker with:

```bash
redis-server
# with docker  
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Celery Worker

Open a new terminal window and run:

```bash
celery -A credimate worker --loglevel=info --pool=solo
```

> **Note:** Use `--pool=solo` for compatibility on Windows.

### 7. Run the Django Development Server

```bash
python manage.py runserver
```
