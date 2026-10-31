# EduTrack — Student Management System

A full-stack, responsive Student Management System web application built with **Python Flask**, **SQLite**, and **SQLAlchemy**, styled using **Tailwind CSS** and **Bootstrap 5.3** with interactive **Chart.js** analytics.

---

## 🌟 Key Features

### 1. Student Records Management (Full CRUD)
- **Add New Students**: Modal-driven registration form capturing:
  - Full Name
  - Roll Number (Unique, alphanumeric)
  - Email Address (Unique, format verified)
  - Phone Number (Validated format)
  - Department (CS, IT, ECE, ME, Civil, Data Science, etc.)
  - Year / Semester
  - Enrollment Status (*Active*, *Inactive*, *Graduated*)
- **Searchable & Filterable Directory**:
  - Instant multi-field search across student names, roll numbers, emails, and phone numbers.
  - Multi-criteria filtering by Department, Semester, and Status.
- **Server-Side Pagination**:
  - Fast, memory-efficient pagination that handles large student datasets with previous/next and page indicators.
- **Edit & Update**:
  - Pre-populated modal editing with asynchronous JSON prefetch.
- **Safe Delete with Prompt**:
  - Confirmation modal clearly displaying the student's name and roll number before permanently deleting records.
- **Data Export**:
  - One-click **Export to CSV** for reports and administrative records.

### 2. Dashboard & Visual Statistics
- **KPI Summary Cards**:
  - Total student enrollment count.
  - Active students with percentage share.
  - Inactive / On-leave count.
  - Graduated alumni count.
- **Interactive Visualizations (Chart.js)**:
  - **Donut Chart**: Department-wise enrollment share with custom tooltips.
  - **Bar Chart**: Cohort distribution across academic years and semesters.
- **Recent Registrations**: Quick-reference table of the latest 5 enrolled students.
- **Department Ratios**: Visual progress bars representing program enrollment density.

### 3. Database & Backend Architecture
- **SQLite Database** with **Flask-SQLAlchemy ORM** for persistent, portable storage.
- **Input Validation & Data Integrity**:
  - Duplicate roll number detection (case-insensitive).
  - Duplicate email detection.
  - Regex-based email and phone number formatting verification.
  - Clean client-side & server-side validation error reporting.
- **RESTful Endpoints & Error Handling**:
  - Friendly custom `404` (Not Found) and `500` (Internal Server Error) templates.
  - JSON API endpoints for AJAX operations and analytics (`/api/stats`, `/students/<id>/json`).

### 4. UI/UX Design
- **Hybrid Tailwind CSS & Bootstrap 5**:
  - Modern dashboard layout with responsive dark sidebar navigation and mobile drawer toggle.
  - Clean card-based design with subtle shadows and rounded corners.
  - Toast notifications and dismissible alerts for user feedback.

---

## 📁 Directory Structure

```
student_management_system/
│
├── app.py                     # Flask application factory, routes, and controllers
├── config.py                  # Application configurations & constants
├── models.py                  # SQLAlchemy Database models (Student entity)
├── forms.py                   # Form validation logic & regex patterns
├── seed.py                    # Database seeder with realistic sample records
├── tests.py                   # Automated unit test suite
├── requirements.txt           # Project Python dependencies
├── README.md                  # Project documentation & run guide
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom styling and scrollbar enhancements
│   └── js/
│       ├── main.js            # Sidebar toggle, AJAX form handling, modals, and toasts
│       └── charts.js          # Chart.js visualization logic for analytics dashboard
│
└── templates/
    ├── base.html              # Base layout (sidebar, navbar, modals, toasts)
    ├── dashboard.html         # Analytics dashboard with metric cards and charts
    ├── students.html          # Student records directory with table, search, and pagination
    ├── 404.html               # Custom 404 Not Found error template
    └── 500.html               # Custom 500 Server Error error template
```

---

## 🚀 Getting Started Locally

### 1. Prerequisites
Ensure you have **Python 3.10+** installed:
```bash
python --version
```

### 2. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database (Optional)
The database auto-creates and seeds upon first launch, or you can run the seeder manually:
```bash
python seed.py
```

### 4. Run the Web Application
Start the Flask development server:
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🧪 Running Automated Tests

Run the test suite to verify database operations, API endpoints, validations, and CSV export:
```bash
python tests.py
```

---

## 📡 API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/dashboard` |
| `GET` | `/dashboard` | Main analytics dashboard page |
| `GET` | `/api/stats` | JSON analytics data for charts |
| `GET` | `/students` | Paginated, searchable student directory |
| `GET` | `/students/<id>/json` | Fetch single student JSON for edit modal |
| `POST` | `/students/add` | Register new student record |
| `POST` | `/students/edit/<id>` | Update an existing student record |
| `POST` | `/students/delete/<id>` | Delete student record |
| `GET` | `/students/export` | Download filtered students list as CSV |

---

## 🛡️ License
Open-source under the MIT License.
