# myapp/tasks.py
from celery import shared_task
import time

@shared_task
def send_welcome_email(user_email):
    # Simulate a heavy or long-running operation (like sending an email)
    time.sleep(5) 
    return f"Email sent successfully to {user_email}"
