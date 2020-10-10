from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from rest_framework import status, request
from rest_framework.test import APIClient, APITestCase, force_authenticate
import mock
from django.core.files import File
from .models import Custom_User, Apartment, Room, Images, Opinion, Address, Advert


# Create your tests here.

class AccountTests(APITestCase):
    file_mock = mock.MagicMock(spec=File, name='FileMock')
    room_images = file_mock
    rooms = [{'name': 'test_room_name', 'description': 'test_room_description', 'price': '350', 'area_metrage': '35',
              'rented': False, 'images': room_images}]

    address = {'street_name': 'test_address_street', 'house_nr': 'test_address_nr', 'country': 'test_address_country',
               'postal_code': 'test_address_postal', 'city': 'test_address_city'}
    name = "test_apartment_name"
    description = "test_apartment_description"
    images = file_mock
    try:
         user = Custom_User.objects.create_user(username='testuser', password='12345')
    except IntegrityError:
        user = Custom_User.objects.get(username='testuser')
    try:
        test_new_apartment = Apartment.objects.create(name=name, description=description, price=1120, owner = Custom_User.objects.get(username=user), rent_as_whole=False)
    except IntegrityError:
        test_new_apartment = Apartment.objects.get(name=name)

    try:
        test_new_opinion = Opinion.objects.create(apartment=test_new_apartment, description='test_opinion_dsc', stats=5, poster = Custom_User.objects.get(username=user))
    except IntegrityError:
        test_new_opinion = Opinion.objects.get(apartment=test_new_apartment)

    try:
        test_new_address = Address.objects.create(street_name=address['street_name'], house_nr=address['house_nr'],
                                                  country=address['country'], postal_code=address['postal_code'],
                                                  city=address['city'], apartment=test_new_apartment)
    except IntegrityError:
        test_new_address = Address.objects.get(apartment=test_new_apartment)

    try:
        test_new_advert = Advert.objects.create(apartment=test_new_apartment, ends_on=(datetime.now() + timedelta(days=10)))
    except IntegrityError:
        test_new_advert = Advert.objects.get(apartment=test_new_apartment)


    try:
        for room in rooms:
            test_single_room = Room.objects.create(name=room['name'], apartment=test_new_apartment,
                                              description=room['description'],
                                              price=room['price'],
                                              area_metrage=room['area_metrage'])
            for image in room['images']:
                Images.objects.create(room=test_single_room, image=image)
    except IntegrityError:
        test_single_room = Room.objects.get(name='test_room_name')


    def setUp(self) -> None:
        self.test_new_opinion.save()
        self.user.save()
        self.test_single_room.save()
        self.test_new_apartment.save()
        self.test_new_address.save()
        self.test_new_advert.save()
        self.client.force_authenticate(user=self.user)

    def test_create_aparment(self):
        price = '1000'
        rent_as_whole = True
        response = self.client.put('/apartment/', {'rooms': self.rooms,'images': self.images,'address': self.address,'name': self.name,'description': self.description,'price': price,'rent_as_whole': rent_as_whole}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_apartment(self):
        response = self.client.get('/apartment/', {'apartment_id': self.test_new_apartment.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_apartment(self):
        response = self.client.delete('/apartment/',data={'apartment_id': self.test_new_apartment.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/apartment/', data={'apartment_id': 123567890}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_apartment(self):
        patch_data = {'description': "new_test_decription", 'price': 900}
        response = self.client.patch('/apartment/', data={'apartment_id': self.test_new_apartment.id, 'patch_data': patch_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_put_room(self):
        response = self.client.put('/room/', {'apartment_id': self.test_new_apartment.id,'images': self.images,'name': 'new_single_room','description': 'new_single_description','price': 150,'area_metrage': 15}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_room(self):
        response = self.client.get('/room/', {'room_id': self.test_single_room.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_room(self):
        response = self.client.delete('/room/',data={'room_id': self.test_single_room.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/room/', data={'room_id': 123567890}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_room(self):
        patch_data = {'description': "new_test_decription", 'price': 900}
        response = self.client.patch('/room/', data={'room_id': self.test_single_room.id, 'patch_data': patch_data}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_opinion(self):
        response = self.client.put('/opinion/', {'id': self.test_new_apartment.id,'type': 'apartment', 'description': 'new_opinion_description','stats': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_opinion(self):
        response = self.client.get('/opinion/', {'id': self.test_new_opinion.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_opinion(self):
        response = self.client.delete('/opinion/',data={'id':  self.test_new_opinion.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/opinion/', data={'id': 123567890}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_opinion(self):
        patch_data = {'description': "new_test_decription"}
        response = self.client.patch('/opinion/', data={'id':  self.test_new_opinion.id, 'patch_data': patch_data}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_put_advert(self):
        response = self.client.put('/advert/', {'id': self.test_new_apartment.id, 'type': 'apartment'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_advert(self):
        response = self.client.get('/advert/', {'id': self.test_new_advert.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_advert(self):
        response = self.client.delete('/advert/', data={'id': self.test_new_advert.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete('/advert/', data={'id': 123567890}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_advert(self):
        patch_data = {'active': False}
        response = self.client.patch('/advert/', data={'id': self.test_new_advert.id, 'patch_data': patch_data},
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

