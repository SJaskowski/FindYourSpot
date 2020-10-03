from django.db.models import Model, ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from pyexpat import model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Apartment, Room, Images, Custom_User


class UserApartment(APIView):
	def put(self, request):
		rooms = request.data['rooms']
		apartment_images = request.data['images']
		address = request.data['address']
		name = request.data['name']
		description = request.data['description']
		price = request.data['price']
		rent_as_whole = request.data['rent_as_whole']
		owner = Custom_User.objects.get(username=request.user.username)
		new_apartment = Apartment.objects.create(name=name, description=description, price=price, owner=owner, rent_as_whole=rent_as_whole, address=address)
		for room in rooms:
			single_room = Room.objects.create(name=room['name'], apartment=new_apartment, description=room['description'],
			                                  price=room['price'],
			                                  area_metrage=room['area_metrage'])
			for image in room['images']:
				Images.objects.create(room=single_room, image=image)
		for image in apartment_images:
			Images.objects.create(aprtment=new_apartment, image=image)
		return Response(status=status.HTTP_201_CREATED)

	def get(self, request):
		apartment_id = request.GET.get('apartment_id')
		rooms_in_apartment = list(Room.objects.filter(apartment=Apartment.objects.get(id=apartment_id)).values())
		apartment = list(Apartment.objects.filter(id=apartment_id).values())[0]

		return Response({'apartment': apartment, 'rooms': rooms_in_apartment})


	def delete(self, request):
		apartment_id = request.data['apartment_id']
		try:
			tmp_apartment = Apartment.objects.get(id=apartment_id)
			tmp_apartment.delete()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


	def patch(self, request):
		apartment_id = request.data['apartment_id']
		patch_data = request.data['patch_data']
		try:
			tmp_apartment = Apartment.objects.get(id=apartment_id)
			for new_data in patch_data.items():
				setattr(tmp_apartment, new_data[0],new_data[1])
				tmp_apartment.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


class UserRoom(APIView):
	def put(self, request):
		apartment_id = request.data['apartment_id']
		area_metrage = request.data['area_metrage']
		name = request.data['name']
		description = request.data['description']
		price = request.data['price']
		images = request.data['images']
		owner = Custom_User.objects.get(username=request.user.username)

		old_apartment = Apartment.objects.get(owner=owner, id=apartment_id)
		print(Room.objects.all())
		new_room = Room.objects.create(name=name, apartment=old_apartment, description=description,
		                                  price=price,
		                                  area_metrage=area_metrage)
		for image in images:
			Images.objects.create(room=new_room, image=image)
		print(Room.objects.all())
		return Response(status=status.HTTP_201_CREATED)

	def get(self, request):
		room_id = request.GET.get('room_id')
		images_in_room = list(Images.objects.filter(room=Room.objects.get(id=room_id)).values())
		room = list(Room.objects.filter(id=room_id).values())[0]

		return Response({'room': room, 'images': images_in_room})


	def delete(self, request):
		room_id = request.data['room_id']
		try:
			tmp_room = Room.objects.get(id=room_id)
			tmp_room.delete()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)


	def patch(self, request):
		room_id = request.data['room_id']
		patch_data = request.data['patch_data']
		try:

			tmp_room = Room.objects.get(id=room_id)
			print(tmp_room.price)
			for new_data in patch_data.items():
				setattr(tmp_room, new_data[0],new_data[1])
				tmp_room.save()
			print(tmp_room.price)
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)