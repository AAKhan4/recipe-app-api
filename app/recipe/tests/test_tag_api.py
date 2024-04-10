'''Tests for the tag API'''
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def create_user(email='user@example.com', password='Testpass123.'):
    '''Create user model'''
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(tag_id):
    '''Return tag detail URL'''
    return reverse('recipe:tag-detail', args=[tag_id])


class PublicTagApiTests(TestCase):
    '''Test unauth tags API'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that auth is required for retrieving tags'''
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    '''Test auth tags API'''

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        ''''Test retrieving tags'''
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        '''Tests tag limited to auth user'''
        user2 = create_user(email='user2@example.com', password='Testpass123.')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tag.name)
        self.assertEqual(response.data[0]['id'], tag.id)

    def test_update_tag(self):
        '''Test updating tag'''
        tag = Tag.objects.create(user=self.user, name='AfterDinner')
        payload = {'name': 'Dessert'}
        url = detail_url(tag.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload.get('name'))

    def test_delete_tag(self):
        '''Test deleting tag'''
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        url = detail_url(tag.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tag = Tag.objects.filter(user=self.user)
        self.assertFalse(tag.exists())

    def test_filter_tags_assigned_to_recipes(self):
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Dinner')
        recipe = Recipe.objects.create(
            title='Green eggs on toast',
            time_mins=10,
            price=Decimal('5.00'),
            user=self.user
        )
        recipe.tags.add(tag1)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, response.data)
        self.assertIn(serializer2.data, response.data)

    def test_filter_tags_assigned_unique(self):
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = Recipe.objects.create(
            title='Green eggs on toast',
            time_mins=10,
            price=Decimal('5.00'),
            user=self.user
        )
        recipe1.tags.add(tag1)
        recipe2 = Recipe.objects.create(
            title='Pancakes',
            time_mins=3,
            price=Decimal('2.00'),
            user=self.user
        )
        recipe2.tags.add(tag1)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(response.data), 1)
