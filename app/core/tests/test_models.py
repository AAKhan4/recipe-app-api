from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model

from core import models


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

    def test_new_user_email_normalised(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'Samplepass123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'samplepass1',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe_success(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='sample recipe',
            time_mins=5,
            price=Decimal('5.50'),
            description='sample description',
        )

        self.assertEqual(str(recipe), recipe.title)
