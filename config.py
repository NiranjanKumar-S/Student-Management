import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-student-mgmt-key-2026'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "students.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STUDENTS_PER_PAGE = 8

    # Standard configuration constants
    DEPARTMENTS = [
        'Computer Science & Engineering',
        'Information Technology',
        'Electronics & Communication',
        'Mechanical Engineering',
        'Civil Engineering',
        'Electrical & Electronics',
        'Business Administration',
        'Data Science & AI'
    ]

    YEARS_SEMESTERS = [
        'Year 1 / Sem 1',
        'Year 1 / Sem 2',
        'Year 2 / Sem 3',
        'Year 2 / Sem 4',
        'Year 3 / Sem 5',
        'Year 3 / Sem 6',
        'Year 4 / Sem 7',
        'Year 4 / Sem 8'
    ]

    ENROLLMENT_STATUSES = ['Active', 'Inactive', 'Graduated']
