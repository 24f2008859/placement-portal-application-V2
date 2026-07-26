from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name, 
        backend = 'redis://localhost:6379/0',
        broker = 'redis://localhost:6379/0'
    )

    celery.conf.update(app.config)

    celery.conf.beat_schedule = {
        'daily-interview-remider': {
            'task': 'tasks.send_interview_reminders',
            'schedule': crontab(hour=9, minute=0),
        },
        'monthly-placement-report': {
            'task': 'tasks.send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=8, minute=0),
        },
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery 