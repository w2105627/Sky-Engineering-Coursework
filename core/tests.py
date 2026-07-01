# Author : w2105627
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Department, Employee, Organisation, Team

#This section implements all my test cases from CWK1
@override_settings(AUTH_PASSWORD_VALIDATORS=[])
class CourseworkTestPlanTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(organisation_name='Sky')
        self.manager = Employee.objects.create(full_name='Olivia Carter')
        self.department = Department.objects.create(
            department_name='xTV_Web',
            department_head=self.manager,
            organisation=self.organisation,
        )
        self.team = Team.objects.create(
            team_name='Code Warriors',
            department=self.department,
            team_leader=self.manager,
            status='Active',
        )

    def register_test_user(self):
        return self.client.post(reverse('accounts:signup'), {
            'full_name': 'Test User',
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test',
        })

    def test_case_1_register_with_valid_input(self):
        response = self.register_test_user()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='test').exists())
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_case_2_register_with_invalid_input(self):
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )

        response = self.register_test_user()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='test').count(), 1)

    def test_case_3_login_with_valid_input(self):
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )

        response = self.client.post(reverse('accounts:login'), {
            'username': 'test',
            'password': 'test',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:teams'))

    def test_case_4_login_with_invalid_input(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'invalid',
            'password': 'invalid',
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_case_5_logout(self):
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        self.client.login(username='test', password='test')

        response = self.client.get(reverse('accounts:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('core:teams'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_case_6_update_email(self):
        user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        Employee.objects.create(user=user, full_name='Test User')
        self.client.login(username='test', password='test')

        response = self.client.post(reverse('accounts:profile'), {
            'update_profile': '1',
            'full_name': 'Test User',
            'username': 'test',
            'email': 'newemail@test.com',
        })

        user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, 'newemail@test.com')

    def test_case_7_update_password(self):
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        self.client.login(username='test', password='test')

        response = self.client.post(reverse('accounts:profile'), {
            'change_password': '1',
            'old_password': 'test',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        })

        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.assertFalse(self.client.login(username='test', password='test'))
        self.assertTrue(self.client.login(username='test', password='newpassword'))

    def test_case_8_search_teams(self):
        User.objects.create_user(
            username='test',
            email='test@test.com',
            password='test',
        )
        self.client.login(username='test', password='test')

        response = self.client.get(reverse('core:teams'), {'q': 'Code Warriors'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Code Warriors')
