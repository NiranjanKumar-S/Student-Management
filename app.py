import io
import csv
from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify, Response
)
from sqlalchemy import or_, func
from config import Config
from models import db, Student
from forms import validate_student_data

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Automatic table initialization and auto-seed on first run
    with app.app_context():
        db.create_all()
        # Seed initial records if database is empty
        if Student.query.count() == 0:
            from seed import SAMPLE_STUDENTS
            for s_data in SAMPLE_STUDENTS:
                student = Student(**s_data)
                db.session.add(student)
            db.session.commit()

    # Context processor to make app configuration easily accessible in templates
    @app.context_processor
    def inject_global_data():
        return {
            'DEPARTMENTS': app.config['DEPARTMENTS'],
            'YEARS_SEMESTERS': app.config['YEARS_SEMESTERS'],
            'ENROLLMENT_STATUSES': app.config['ENROLLMENT_STATUSES']
        }

    # ==========================================
    # ROUTES
    # ==========================================

    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    # ------------------------------------------
    # 1. Dashboard & Analytics
    # ------------------------------------------
    @app.route('/dashboard')
    def dashboard():
        # Core Metrics
        total_students = Student.query.count()
        active_count = Student.query.filter_by(status='Active').count()
        inactive_count = Student.query.filter_by(status='Inactive').count()
        graduated_count = Student.query.filter_by(status='Graduated').count()

        # Department distribution
        dept_counts_query = (
            db.session.query(Student.department, func.count(Student.id))
            .group_by(Student.department)
            .order_by(func.count(Student.id).desc())
            .all()
        )
        dept_data = [{'department': dept, 'count': count} for dept, count in dept_counts_query]

        # Year/Semester distribution
        year_counts_query = (
            db.session.query(Student.year_semester, func.count(Student.id))
            .group_by(Student.year_semester)
            .all()
        )
        year_data = [{'year_semester': ys, 'count': count} for ys, count in year_counts_query]

        # Recent 5 students
        recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()

        return render_template(
            'dashboard.html',
            total_students=total_students,
            active_count=active_count,
            inactive_count=inactive_count,
            graduated_count=graduated_count,
            dept_data=dept_data,
            year_data=year_data,
            recent_students=recent_students
        )

    # API Endpoint for dynamic chart refreshes
    @app.route('/api/stats')
    def api_stats():
        # Department counts
        dept_counts = (
            db.session.query(Student.department, func.count(Student.id))
            .group_by(Student.department)
            .all()
        )
        # Year / Semester counts
        year_counts = (
            db.session.query(Student.year_semester, func.count(Student.id))
            .group_by(Student.year_semester)
            .all()
        )
        # Status counts
        status_counts = (
            db.session.query(Student.status, func.count(Student.id))
            .group_by(Student.status)
            .all()
        )

        return jsonify({
            'departments': {
                'labels': [d[0] for d in dept_counts],
                'data': [d[1] for d in dept_counts]
            },
            'years': {
                'labels': [y[0] for y in year_counts],
                'data': [y[1] for y in year_counts]
            },
            'statuses': {
                'labels': [s[0] for s in status_counts],
                'data': [s[1] for s in status_counts]
            }
        })

    # ------------------------------------------
    # 2. Student Records Management (CRUD)
    # ------------------------------------------
    @app.route('/students')
    def student_list():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str).strip()
        dept_filter = request.args.get('department', '', type=str).strip()
        year_filter = request.args.get('year_semester', '', type=str).strip()
        status_filter = request.args.get('status', '', type=str).strip()
        sort_by = request.args.get('sort_by', 'created_at', type=str)
        sort_order = request.args.get('order', 'desc', type=str)

        query = Student.query

        # Multi-field search
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Student.full_name.ilike(search_pattern),
                    Student.roll_number.ilike(search_pattern),
                    Student.email.ilike(search_pattern),
                    Student.phone_number.ilike(search_pattern)
                )
            )

        # Filters
        if dept_filter:
            query = query.filter(Student.department == dept_filter)
        if year_filter:
            query = query.filter(Student.year_semester == year_filter)
        if status_filter:
            query = query.filter(Student.status == status_filter)

        # Sorting
        sort_column = getattr(Student, sort_by, Student.created_at)
        if sort_order == 'asc':
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        per_page = app.config.get('STUDENTS_PER_PAGE', 8)
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            'students.html',
            students=pagination.items,
            pagination=pagination,
            search=search,
            dept_filter=dept_filter,
            year_filter=year_filter,
            status_filter=status_filter,
            sort_by=sort_by,
            sort_order=sort_order
        )

    # API: Fetch single student for edit modal
    @app.route('/students/<int:student_id>/json')
    def get_student_json(student_id):
        student = db.get_or_404(Student, student_id)
        return jsonify(student.to_dict())

    # Create Student
    @app.route('/students/add', methods=['POST'])
    def add_student():
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        data = request.get_json() if request.is_json else request.form

        is_valid, errors, cleaned = validate_student_data(data)

        if not is_valid:
            if is_ajax:
                return jsonify({'success': False, 'errors': errors}), 400
            for field, err in errors.items():
                flash(err, 'danger')
            return redirect(url_for('student_list'))

        new_student = Student(
            full_name=cleaned['full_name'],
            roll_number=cleaned['roll_number'],
            email=cleaned['email'],
            phone_number=cleaned['phone_number'],
            department=cleaned['department'],
            year_semester=cleaned['year_semester'],
            status=cleaned['status']
        )
        db.session.add(new_student)
        db.session.commit()

        if is_ajax:
            return jsonify({
                'success': True,
                'message': f'Student {new_student.full_name} ({new_student.roll_number}) added successfully!',
                'student': new_student.to_dict()
            })

        flash(f'Student "{new_student.full_name}" registered successfully!', 'success')
        return redirect(url_for('student_list'))

    # Update Student
    @app.route('/students/edit/<int:student_id>', methods=['POST'])
    def edit_student(student_id):
        student = db.get_or_404(Student, student_id)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        data = request.get_json() if request.is_json else request.form

        is_valid, errors, cleaned = validate_student_data(data, student_id=student.id)

        if not is_valid:
            if is_ajax:
                return jsonify({'success': False, 'errors': errors}), 400
            for field, err in errors.items():
                flash(err, 'danger')
            return redirect(url_for('student_list'))

        student.full_name = cleaned['full_name']
        student.roll_number = cleaned['roll_number']
        student.email = cleaned['email']
        student.phone_number = cleaned['phone_number']
        student.department = cleaned['department']
        student.year_semester = cleaned['year_semester']
        student.status = cleaned['status']

        db.session.commit()

        if is_ajax:
            return jsonify({
                'success': True,
                'message': f'Student "{student.full_name}" updated successfully!',
                'student': student.to_dict()
            })

        flash(f'Student "{student.full_name}" updated successfully!', 'success')
        return redirect(url_for('student_list'))

    # Delete Student
    @app.route('/students/delete/<int:student_id>', methods=['POST'])
    def delete_student(student_id):
        student = db.get_or_404(Student, student_id)
        student_name = student.full_name
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json

        db.session.delete(student)
        db.session.commit()

        if is_ajax:
            return jsonify({
                'success': True,
                'message': f'Student record for "{student_name}" was permanently deleted.'
            })

        flash(f'Student "{student_name}" has been removed.', 'info')
        return redirect(url_for('student_list'))

    # Export to CSV feature
    @app.route('/students/export')
    def export_students_csv():
        students = Student.query.order_by(Student.roll_number.asc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Roll Number', 'Full Name', 'Email', 'Phone Number', 'Department', 'Year/Semester', 'Status', 'Registration Date'])

        for s in students:
            writer.writerow([
                s.id,
                s.roll_number,
                s.full_name,
                s.email,
                s.phone_number,
                s.department,
                s.year_semester,
                s.status,
                s.created_at.strftime('%Y-%m-%d %H:%M') if s.created_at else ''
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=students_directory.csv"}
        )

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
