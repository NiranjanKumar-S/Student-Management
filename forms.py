import re
from models import Student

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
PHONE_REGEX = r'^\+?[0-9\s\-()]{7,20}$'

def validate_student_data(data, student_id=None):
    """
    Validates student form data.
    Returns: (is_valid: bool, errors: dict, cleaned_data: dict)
    """
    errors = {}
    cleaned = {}

    # Full Name
    name = (data.get('full_name') or '').strip()
    if not name:
        errors['full_name'] = 'Full Name is required.'
    elif len(name) < 2 or len(name) > 100:
        errors['full_name'] = 'Name must be between 2 and 100 characters.'
    cleaned['full_name'] = name

    # Roll Number
    roll_number = (data.get('roll_number') or '').strip().upper()
    if not roll_number:
        errors['roll_number'] = 'Roll Number is required.'
    elif not re.match(r'^[A-Z0-9\-_]{2,20}$', roll_number, re.IGNORECASE):
        errors['roll_number'] = 'Roll Number must be 2-20 alphanumeric characters (hyphens and underscores allowed).'
    else:
        # Check uniqueness
        query = Student.query.filter(Student.roll_number.ilike(roll_number))
        if student_id:
            query = query.filter(Student.id != student_id)
        if query.first():
            errors['roll_number'] = f'Roll Number "{roll_number}" is already registered.'
    cleaned['roll_number'] = roll_number

    # Email
    email = (data.get('email') or '').strip().lower()
    if not email:
        errors['email'] = 'Email address is required.'
    elif not re.match(EMAIL_REGEX, email):
        errors['email'] = 'Please enter a valid email address (e.g., student@example.edu).'
    else:
        # Check uniqueness
        query = Student.query.filter(Student.email.ilike(email))
        if student_id:
            query = query.filter(Student.id != student_id)
        if query.first():
            errors['email'] = f'Email address "{email}" is already registered.'
    cleaned['email'] = email

    # Phone Number
    phone = (data.get('phone_number') or '').strip()
    digits_only = re.sub(r'\D', '', phone)
    if not phone:
        errors['phone_number'] = 'Phone Number is required.'
    elif not re.match(PHONE_REGEX, phone) or len(digits_only) < 7 or len(digits_only) > 15:
        errors['phone_number'] = 'Please enter a valid phone number (7 to 15 digits).'
    cleaned['phone_number'] = phone

    # Department
    dept = (data.get('department') or '').strip()
    if not dept:
        errors['department'] = 'Department is required.'
    cleaned['department'] = dept

    # Year / Semester
    year_sem = (data.get('year_semester') or '').strip()
    if not year_sem:
        errors['year_semester'] = 'Year / Semester is required.'
    cleaned['year_semester'] = year_sem

    # Status
    status = (data.get('status') or 'Active').strip().capitalize()
    if status not in ['Active', 'Inactive', 'Graduated']:
        status = 'Active'
    cleaned['status'] = status

    return len(errors) == 0, errors, cleaned
