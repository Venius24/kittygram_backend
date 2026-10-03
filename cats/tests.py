from datetime import date

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Cat


class CatApiTests(APITestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user('owner', password='testpass123')
        self.other = get_user_model().objects.create_user('other', password='testpass123')
        self.cat = Cat.objects.create(name='Murka', color='white', birth_year=2020, owner=self.owner)

    def test_only_owner_can_change_cat(self):
        self.client.force_authenticate(self.other)
        response = self.client.patch(f'/api/cats/{self.cat.id}/', {'name': 'Changed'})
        self.assertEqual(response.status_code, 403)
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.name, 'Murka')

    def test_patch_achievements_and_validate_year(self):
        self.client.force_authenticate(self.owner)
        url = f'/api/cats/{self.cat.id}/'
        response = self.client.patch(url, {'achievements': [{'achievement_name': 'Playful'}]}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(self.cat.achievements.values_list('name', flat=True)), ['Playful'])
        response = self.client.patch(url, {'birth_year': date.today().year + 1}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_local_frontend_origin_is_allowed(self):
        response = self.client.options(
            '/api/cats/',
            HTTP_ORIGIN='http://127.0.0.1:3000',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET',
        )
        self.assertEqual(
            response.get('Access-Control-Allow-Origin'),
            'http://127.0.0.1:3000',
        )
