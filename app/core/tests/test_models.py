from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelsTest(TestCase):
    def test_create_user_with_email_success(self):
        email = 'testmail@example.com'
        password = 'examplePass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))