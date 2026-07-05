from app import create_app, db
from models import User 

app = create_app()

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email='admin@placeme.com').first()

    if not admin:
        admin = User(
            email = 'admin@placeme.com',
            password = 'admin123',
            role = 'admin'
        )
        db.session.add(admin)
        db.session.commit()
    else:
        print("Admin user already exists")

    print("Database tables created successfully")