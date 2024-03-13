from celery import shared_task
from time import sleep
from django.conf import settings
from .models import UserAccount


from django.core.mail import send_mail

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task
def send_mail_task_with_celery(subject,email,message):
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,email_from,recipient_list)
    return None


@shared_task()
def task_schedular():
    users=UserAccount.objects.all()
    # print('email------------',users.email)
    for user in users:
        mail_subject='Easy find a doctor according to your requirements'
        message='we have a lot of doctor with different in there field and specialist'
        to_email=user.email
        send_mail(subject=mail_subject,
                  message=message,
                  from_email=settings.EMAIL_HOST_USER,
                #   recipient_list=['sakibcse7@gmail.com'],
                  recipient_list=[to_email],
                  fail_silently=True
                  
        )

    return "Done"