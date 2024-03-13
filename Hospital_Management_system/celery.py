import os



from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hospital_Management_system.settings')

app = Celery('Hospital_Management_system')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')





#  celery beat setting
app.conf.beat_schedule={
    'send-mail-everyday':{
    'task':'Doctor.task.task_schedular',
    'schedule': crontab(minute='*/3'),
    # 'args':()

    
    }
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')