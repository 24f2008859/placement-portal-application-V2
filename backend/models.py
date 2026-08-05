from app import db 
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    role = db.Column(db.String(20), nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    student_profile = db.relationship('Student', backref='user', uselist=False)
    company_profile = db.relationship('Company', backref='user', uselist = False)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    full_name = db.Column(db.String(100), nullable = False)
    education = db.Column(db.String(200))
    skills = db.Column(db.String(300))
    resume = db.Column(db.String(200))
    cgpa = db.Column(db.Float)
    branch = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    applications = db.relationship('Application', backref='student', lazy=True)
    is_active = db.Column(db.Boolean, default = True)

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    website = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    jobs = db.relationship('Job', backref='company', lazy= True)
    is_active = db.Column(db.Boolean, default = True)

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key = True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable = False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    skills_required = db.Column(db.Text)
    salary = db.Column(db.Float)
    location = db.Column(db.String(100))
    minimum_cgpa = db.Column(db.Float)
    eligible_branch = db.Column(db.String(100))
    eligible_year = db.Column(db.Integer)
    application_deadline = db.Column(db.DateTime) 
    status = db.Column(db.String(20), default = 'pending')
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    applications = db.relationship('Application', backref='job', lazy = True) 

class Application(db.Model):
    __tablename__ = 'applications'

    __table_args__ = (
        UniqueConstraint(
            'student_id',
            'job_id',
            name='unique_student_job_application'
        ),
    )

    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable = False)
    status = db.Column(db.String(20), default='applied')
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notified = db.Column(db.Boolean, default = True)
    placement = db.relationship('Placement', backref='application', uselist=False)


class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key = True)

    application_id = db.Column(
        db.Integer,
        db.ForeignKey('applications.id'),
        nullable = False
    )

    interview_date = db.Column(db.DateTime, nullable=False)

    mode = db.Column(
        db.String(50),
        default = 'online'
    )

    meeting_link = db.Column(db.String(300))

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    application = db.relationship(
        'Application',
        backref=db.backref('interview', uselist=False)
    )

class Placement(db.Model):
    __tablename__ = 'placements'

    id = db.Column(db.Integer, primary_key = True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable = False)
    salary = db.Column(db.Float)
    joining_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    company = db.relationship('Company', foreign_keys = [company_id])
    student = db.relationship('Student', foreign_keys=[student_id])