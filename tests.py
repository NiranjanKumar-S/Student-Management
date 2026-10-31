import unittest
import json
from app import create_app
from models import db, Student

class StudentManagementSystemTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_dashboard_route(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analytics Dashboard', response.data)

    def test_stats_api(self):
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('departments', data)
        self.assertIn('years', data)
        self.assertIn('statuses', data)

    def test_students_directory(self):
        response = self.client.get('/students')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Records Directory', response.data)

    def test_add_and_delete_student(self):
        # 1. Add student
        new_student = {
            'full_name': 'Test Student Unit',
            'roll_number': 'TEST-999',
            'email': 'test.unit@campus.edu',
            'phone_number': '+1 555-999-0000',
            'department': 'Computer Science & Engineering',
            'year_semester': 'Year 1 / Sem 1',
            'status': 'Active'
        }
        res = self.client.post('/students/add', data=json.dumps(new_student),
                               content_type='application/json',
                               headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res.status_code, 200)
        res_data = res.get_json()
        self.assertTrue(res_data['success'])
        student_id = res_data['student']['id']

        # 2. Duplicate roll number check
        dup_res = self.client.post('/students/add', data=json.dumps(new_student),
                                  content_type='application/json',
                                  headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(dup_res.status_code, 400)
        dup_data = dup_res.get_json()
        self.assertIn('roll_number', dup_data['errors'])

        # 3. Edit student
        edit_data = {
            'full_name': 'Test Student Renamed',
            'roll_number': 'TEST-999',
            'email': 'test.unit@campus.edu',
            'phone_number': '+1 555-999-0000',
            'department': 'Data Science & AI',
            'year_semester': 'Year 1 / Sem 2',
            'status': 'Active'
        }
        edit_res = self.client.post(f'/students/edit/{student_id}', data=json.dumps(edit_data),
                                   content_type='application/json',
                                   headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(edit_res.status_code, 200)
        self.assertEqual(edit_res.get_json()['student']['department'], 'Data Science & AI')

        # 4. Delete student
        del_res = self.client.post(f'/students/delete/{student_id}',
                                   headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(del_res.status_code, 200)
        self.assertTrue(del_res.get_json()['success'])

    def test_export_csv(self):
        response = self.client.get('/students/export')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')
        self.assertIn(b'Roll Number,Full Name,Email', response.data)

if __name__ == '__main__':
    unittest.main()
