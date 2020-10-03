from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class Apartment(APIView):
	def put(self, request):
		rooms = request.data['rooms']
		apartment_images = request.data['images']
		address = request.data['address']
		name = request.data['name']
		description = request.data['description']
		price = request.data['price']
		owner = request.data['owner']
		rent_as_whole = request.data['rent_as_whole']
		new_apartment = Apartment.objects.create(name=name, description=description, price=price, owner=owner, rent_as_whole=rent_as_whole, address=address)

		for room in rooms:
			single_room = Room.objects.create(name=room['name'], apartment=new_apartment, description=room['description'], price=room['price'], area_metrage=room['area_metrage'])
			for image in room['images']:
				Images.objects.create(room=single_room, image=image)
		for image in apartment_images:
			Images.objects.create(aprtment=new_apartment, image=image)


		return Response()

	def get(self, request):
		pass


	def delete(self, request):
		pass

