from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_utc_now():
    return datetime.now(timezone.utc)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(25), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year_semester = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Active', nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)
    updated_at = db.Column(db.DateTime, default=get_utc_now, onupdate=get_utc_now)

    def to_dict(self):
        return {
            'id': self.id,
            'roll_number': self.roll_number,
            'full_name': self.full_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'department': self.department,
            'year_semester': self.year_semester,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else ''
        }

    def __repr__(self):
        return f'<Student {self.roll_number} - {self.full_name}>'
