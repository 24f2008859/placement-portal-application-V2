# Placeme V2 - Campus Placement Management System
A full-stack placement management portal built with Flask REST API and VueJS frontend.

## Tech Stack

### Backend
- Flask (REST API)
- SQLAlchemy (ORM)
- SQLite (Database)
- Redis (Caching)
- Celery (Background Jobs)
- Flask-JWT-Extended (Authentication)
- Flask-Mail (Email Notifications)
- Flask-CORS (Cross-Origin Resource Sharing)

### Frontend
- VueJS 3
- Vue Router
- Bootstrap 5
- Chart.js (Analytics)

## Project Structure

backend/
    - app.py (Flask app factory)
    - models.py (Database models)
    - auth.py (Authentication routes)
    - admin.py (Admin routes)
    - company.py (Company routes)
    - student.py (Student routes)
    - public.py (Public routes)
    - tasks.py (Celery tasks)
    - config.py (Configuration)
    - create_db.py (DB initialization)


frontend/
    - views/ (Vue page components)
    - components/ (Reusable components)
    - router/ (Vue Router config)

## Roles

### Admin
- Pre-created programmatically
- Approve/reject company registration
- Approve/reject placement drives
- View all students, companies, applications
- Search students and companies
- Blacklist/deactivate accounts
- View analytics charts
- Trigger daily reminders
- Generate monthly reports

### Company
- Register and login (after admin approval)
- Create, edit, close, delete placement drives
- View and manage student applications
- Shortlist, interview, select or reject candidates

### Student
- Register and login
- View and apply for approved placement drives
- Track application status
- Upload resume
- Export application history as CSV
- View placement history

## Setup Instructions

### Prerequisites
- Python
- Node.js
- Redis
- Mailpit (for mail testing)

### Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 create_db.py
python3 run.py
```
### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
### Celery Worker
```bash
cd backend
source .venv/bin/activate
celery -A tasks worker --loglevel=info
```
### Redis
```bash
sudo service redis-server start
```
### Mailpit (Email Testing)
```bash
mailpit
```
## Default Admin Credentials
- Email: admin@placeme.com  
- Password: admin123

## API ENdpoints

### Auth
- POST /auth/register/student
- POST /auth/register/company
- POST /auth/login

### Admin
- GET /admin/dashbaord/stats
- GET /admin/companies/pending
- PUT /admin/companies/<id>/approve
- DELETE /admin/companies/<id>/remove
- GET /admin/students/search
- GET /admin/jobs
- PUT /admin/jobs/<id>/approve

### Company
- GET /company/dashbaord
- POST /company/jobs
- GET /company/jobs
- PUT /company/jobs/<id>
- DELETE /company/jobs/<id>
- GET /company/jobs/<id>/applications
- PUT /company/applications/<id>/status

### Student
- GET /student/profile
- PUT /student/profile
- POST /student/resume
- GET /student/jobs
- POST /student/jobs/<id>/apply
- GET /student/applications
- GET /student/placements
- POST /student/export

## Background Jobs (Celery)
- Daily interview reminders (9:00 AM)
- Monthly placement report (1st of every month)
- CSV export (user triggered)

## Caching (Redis)
- Admin dashboard stats (5 min expiry)
- Approved jobs list (5 min expiry)
