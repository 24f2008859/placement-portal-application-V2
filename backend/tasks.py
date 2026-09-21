from celery import Celery
from celery.schedules import crontab
import sys
import os 

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db 
flask_app = create_app()

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.beat_schedule = {
    'daily-interview-reminder': {
        'task': 'tasks.send_interview_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    'monthly-placement-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

@celery.task
def send_interview_reminders():
    with flask_app.app_context():
        from models import Application
        from flask_mail import Message
        from app import mail 

        interviews = Application.query.filter_by(status='interview').all()

        for application in interviews:
            student_email = application.student.user.email
            job_title = application.job.title
            company_name = application.job.company.name

            msg = Message(
                subject=f"Interview Reminder - {job_title} at {company_name}",
                recipients=[student_email],
                body=f"Dear Student, \n\nThis is a reminder that you have an interview for {job_title} at {company_name}.\n\nBest regards, \nPlaceME Team"
            )
            mail.send(msg)
            print(f"Reminder sent to {student_email}")

        return f"Reminders sent to {len(interviews)} students"

@celery.task 
def send_monthly_report(): 
    with flask_app.app_context():
        from models import Application, Placement, User
        from flask_mail import Message
        from app import mail
        from datetime import datetime, timezone

        current_month = datetime.now(timezone.utc).month
        current_year = datetime.now(timezone.utc).year

        total_applications = Application.query.count()
        total_placements = Placement.query.count()

        report_html = f"""
        <html>
        <body>
        <h1>Monthly Placement Report - {current_month}/{current_year}</h1>
        <p>Total Applications: {total_applications}</p>
        <p>Total Placements: {total_placements}</p>
        </body>
        </html>
        """

        admin = User.query.filter_by(role='admin').first()

        msg = Message(
            subject=f"Monthly Placement Report - {current_month}/{current_year}",
            recipients=[admin.email],
            html=report_html 
        )
        mail.send(msg)

        return "Monthly report sent to admin"

@celery.task
def export_applications_csv(student_id): 
    with flask_app.app_context():
        from models import Application, Student
        import csv 

        student = Student.query.get(student_id)
        applications = Application.query.filter_by(student_id=student_id).all()

        filename = f"export_student_{student_id}.csv"
        filepath = os.path.join('static', 'exports', filename)
        os.makedirs(os.path.join('static', 'exports'), exist_ok=True)

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Student ID', 'Company', 'Job Title', 'Status', 'Applied At'])

            for app in applications:
                writer.writerow([
                    student.id,
                    app.job.company.name,
                    app.job.title,
                    app.status,
                    app.applied_at.strftime('%Y-%m-%d')
                ])
        return filename
    