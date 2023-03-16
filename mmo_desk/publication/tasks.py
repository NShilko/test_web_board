from celery import shared_task
from .send_email import send_email_7days


@shared_task
def send_week_news():
    send_email_7days()
