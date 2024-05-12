from django.test import TestCase, Client
from django.urls import reverse

from Lender.models import FairTradeLender
from current import add_cur_user, get_cur_user

class ContactUsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_us_view(self):
        # Make a GET request to the contact_us view
        response = self.client.get(reverse('contact_us'))

        # Check if the view returns a 200 OK status code
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected template
        self.assertTemplateUsed(response, 'ContactUs.html')


class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_us_view(self):
        # Make a GET request to the contact_us view
        response = self.client.get(reverse('about'))

        # Check if the view returns a 200 OK status code
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the expected template
        self.assertTemplateUsed(response, 'About.html')

from django.test import TestCase, Client
from django.urls import reverse
import requests

class RegBorrowViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_reg_borrow_view(self):
        response = self.client.post(reverse('reg_borrow'), {
            'education': 'IITB',
            'capital': 100,
            'income': 200,
            'debt': 300,
            'interest': 5,
            'credit_score': 790,
        })

        self.assertRedirects(response, reverse('home_borrow'))

        self.assertTrue(FairTradeLender.objects.exists())

    def test_home_borrow_view(self):
        FairTradeLender.objects.create(username='test_user')
        response = self.client.get(reverse('home_borrow'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Home_Borrow.html')
        self.assertTrue('users_list' in response.context)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view_redirect_authenticated_user(self):
        user = FairTradeLender.objects.create(username='test_user', password='test_password')
        add_cur_user(user.get_data())
        response = self.client.get(reverse('login_view'))
        self.assertRedirects(response, reverse('borrow/home_borrow'))

    def test_login_view_redirect_authenticated_lender(self):
        user = FairTradeLender.objects.create(username='test_user', password='test_password', account_type=True)
        add_cur_user(user.get_data())
        response = self.client.get(reverse('login_view'))
        self.assertRedirects(response, reverse('lend/home_lend'))

    def test_login_view_post(self):
        user = FairTradeLender.objects.create(username='test_user', password='test_password')
        response = self.client.post(reverse('login_view'), {'username': 'test_user', 'password': 'test_password'})
        self.assertRedirects(response, reverse('lend/home_lend'))

    def test_logout_view(self):
        user = FairTradeLender.objects.create(username='test_user', password='test_password')
        add_cur_user(user.get_data())
        response = self.client.get(reverse('logout_view'))
        self.assertRedirects(response, '/')
        self.assertIsNone(get_cur_user())