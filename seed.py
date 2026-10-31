"""
Seed script to populate the SQLite database with realistic initial student records.
"""
from app import create_app
from models import db, Student

SAMPLE_STUDENTS = [
    {
        "roll_number": "CS2023-001",
        "full_name": "Aarav Sharma",
        "email": "aarav.sharma@campus.edu",
        "phone_number": "+1 (555) 234-5671",
        "department": "Computer Science & Engineering",
        "year_semester": "Year 3 / Sem 5",
        "status": "Active"
    },
    {
        "roll_number": "CS2023-002",
        "full_name": "Sophia Chen",
        "email": "sophia.chen@campus.edu",
        "phone_number": "+1 (555) 345-6782",
        "department": "Computer Science & Engineering",
        "year_semester": "Year 3 / Sem 6",
        "status": "Active"
    },
    {
        "roll_number": "IT2024-015",
        "full_name": "Liam Johnson",
        "email": "liam.j@campus.edu",
        "phone_number": "+1 (555) 456-7893",
        "department": "Information Technology",
        "year_semester": "Year 2 / Sem 3",
        "status": "Active"
    },
    {
        "roll_number": "EC2022-044",
        "full_name": "Priya Patel",
        "email": "priya.patel@campus.edu",
        "phone_number": "+1 (555) 567-8904",
        "department": "Electronics & Communication",
        "year_semester": "Year 4 / Sem 7",
        "status": "Active"
    },
    {
        "roll_number": "ME2021-089",
        "full_name": "Marcus Aurelius Vance",
        "email": "marcus.v@campus.edu",
        "phone_number": "+1 (555) 678-9015",
        "department": "Mechanical Engineering",
        "year_semester": "Year 4 / Sem 8",
        "status": "Graduated"
    },
    {
        "roll_number": "DS2024-003",
        "full_name": "Elena Rostova",
        "email": "elena.r@campus.edu",
        "phone_number": "+1 (555) 789-0126",
        "department": "Data Science & AI",
        "year_semester": "Year 1 / Sem 2",
        "status": "Active"
    },
    {
        "roll_number": "CV2023-012",
        "full_name": "Carlos Gomez",
        "email": "carlos.g@campus.edu",
        "phone_number": "+1 (555) 890-1237",
        "department": "Civil Engineering",
        "year_semester": "Year 2 / Sem 4",
        "status": "Active"
    },
    {
        "roll_number": "BA2022-031",
        "full_name": "Zainab Al-Mansoor",
        "email": "zainab.m@campus.edu",
        "phone_number": "+1 (555) 901-2348",
        "department": "Business Administration",
        "year_semester": "Year 3 / Sem 5",
        "status": "Active"
    },
    {
        "roll_number": "EE2023-019",
        "full_name": "David Kim",
        "email": "david.kim@campus.edu",
        "phone_number": "+1 (555) 123-4569",
        "department": "Electrical & Electronics",
        "year_semester": "Year 2 / Sem 3",
        "status": "Inactive"
    },
    {
        "roll_number": "CS2024-022",
        "full_name": "Fatima Zahra",
        "email": "fatima.z@campus.edu",
        "phone_number": "+1 (555) 987-6540",
        "department": "Computer Science & Engineering",
        "year_semester": "Year 1 / Sem 1",
        "status": "Active"
    },
    {
        "roll_number": "DS2023-011",
        "full_name": "Lucas Silva",
        "email": "lucas.silva@campus.edu",
        "phone_number": "+1 (555) 876-5431",
        "department": "Data Science & AI",
        "year_semester": "Year 2 / Sem 4",
        "status": "Active"
    },
    {
        "roll_number": "IT2022-008",
        "full_name": "Emily Watson",
        "email": "emily.w@campus.edu",
        "phone_number": "+1 (555) 765-4322",
        "department": "Information Technology",
        "year_semester": "Year 4 / Sem 7",
        "status": "Graduated"
    }
]

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        if Student.query.count() == 0:
            print("[INFO] Seeding initial student records...")
            for s_data in SAMPLE_STUDENTS:
                student = Student(**s_data)
                db.session.add(student)
            db.session.commit()
            print(f"[SUCCESS] Successfully seeded {len(SAMPLE_STUDENTS)} students into SQLite database!")
        else:
            print(f"[INFO] Database already contains {Student.query.count()} students. Skipping seed.")

if __name__ == '__main__':
    seed_database()
