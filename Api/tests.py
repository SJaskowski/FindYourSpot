from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status, request
from rest_framework.test import APIClient, APITestCase, force_authenticate
import mock
from django.core.files import File
from .models import Custom_User, Apartment


# Create your tests here.

class AccountTests(APITestCase):
    try:
         user = Custom_User.objects.create_user(username='testuser', password='12345')
    except IntegrityError:
        user = Custom_User.objects.get(username='testuser')
    def test_create_aparment(self):
        self.user.save()
        self.client.force_authenticate(user=self.user)
        file_mock = mock.MagicMock(spec=File, name='FileMock')
        room_images = file_mock
        rooms = [{'name': 'test_room_name', 'description': 'test_room_description', 'price': '350', 'area_metrage': '35', 'rented': False, 'images': room_images}]
        images = file_mock
        address = {'street_name': 'test_address_street', 'house_nr': 'test_address_nr', 'country': 'test_address_country', 'postal_code': 'test_address_postal', 'city': 'test_address_city'}
        name = "test_apartment_name"
        description = "test_apartment_description"
        price = '1000'
        rent_as_whole = True
        response = self.client.put('/apartment/', {'rooms': rooms,'images': images,'address': address,'name': name,'description': description,'price': price,'rent_as_whole': rent_as_whole}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)