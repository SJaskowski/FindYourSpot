from django.db.models import Model, ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from pyexpat import model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Apartment, Room, Images, Custom_User, Address, Opinion


class UserApartment(APIView):
	def put(self, request):
		try:
			rooms = request.data['rooms']
			apartment_images = request.data['images']
			address = request.data['address']
			name = request.data['name']
			description = request.data['description']
			price = request.data['price']
			rent_as_whole = request.data['rent_as_whole']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		owner = Custom_User.objects.get(username=request.user.username)
		new_apartment = Apartment.objects.create(name=name, description=description, price=price, owner=owner, rent_as_whole=rent_as_whole)
		Address.objects.create(street_name=address['street_name'], house_nr=address['house_nr'],
		                                     country=address['country'], postal_code=address['postal_code'],
		                                     city=address['city'], apartment=new_apartment)
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
		try:
			apartment_id = request.GET.get('apartment_id')
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			rooms_in_apartment = list(Room.objects.filter(apartment=Apartment.objects.get(id=apartment_id)).values())
			apartment = list(Apartment.objects.filter(id=apartment_id).values())[0]
			address = list(Address.objects.filter(apartment=Apartment.objects.get(id=apartment_id)).values())
			print(address)
		except ObjectDoesNotExist or IndexError:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response({'apartment': apartment, 'rooms': rooms_in_apartment, 'address': address})


	def delete(self, request):
		try:
			apartment_id = request.data['apartment_id']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			tmp_apartment = Apartment.objects.get(id=apartment_id)
			tmp_apartment.delete()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist or UnboundLocalError:
			return Response(status=status.HTTP_404_NOT_FOUND)


	def patch(self, request):
		try:
			apartment_id = request.data['apartment_id']
			patch_data = request.data['patch_data']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
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
		try:
			apartment_id = request.data['apartment_id']
			area_metrage = request.data['area_metrage']
			name = request.data['name']
			description = request.data['description']
			price = request.data['price']
			images = request.data['images']
			owner = Custom_User.objects.get(username=request.user.username)
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			old_apartment = Apartment.objects.get(owner=owner, id=apartment_id)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		new_room = Room.objects.create(name=name, apartment=old_apartment, description=description,
		                                  price=price,
		                                  area_metrage=area_metrage)
		for image in images:
			Images.objects.create(room=new_room, image=image)
		return Response(status=status.HTTP_201_CREATED)

	def get(self, request):
		try:
			room_id = request.GET.get('room_id')
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)

		try:
			room = list(Room.objects.filter(id=room_id).values())[0]
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		try:
			images_in_room = list(Images.objects.filter(room=Room.objects.get(id=room_id)).values())
		except ObjectDoesNotExist:
			return Response({'room': room})
		return Response({'room': room, 'images': images_in_room})


	def delete(self, request):
		try:
			room_id = request.data['room_id']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			tmp_room = Room.objects.get(id=room_id)
			tmp_room.delete()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist or UnboundLocalError:
			return Response(status=status.HTTP_404_NOT_FOUND)


	def patch(self, request):
		try:
			room_id = request.data['room_id']
			patch_data = request.data['patch_data']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
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

class UserOpinion(APIView):
	def put(self, request):
		try:
			id = request.data['id']
			description = request.data['description']
			stats = request.data['stats']
			type = request.data['type']
			poster = Custom_User.objects.get(username=request.user.username)
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			if type == 'apartment':
				apartment = Apartment.objects.get(id=id)
				Opinion.objects.create(apartment=apartment, description=description,
				                       stats=stats,
				                       poster=poster)
			else:
				if type == 'room':
					room = Room.objects.get(id=id)
					Opinion.objects.create(room=room, description=description,
					                       stats=stats,
					                       poster=poster)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		return Response(status=status.HTTP_201_CREATED)

	def get(self, request):
		try:
			id = request.GET.get('id')
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)

		try:
			opinons = list(Opinion.objects.filter(id=id).values())
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		return Response({'opinons': opinons})


	def delete(self, request):
		try:
			id = request.data['id']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			tmp_opinion = Opinion.objects.get(id=id)
			tmp_opinion.delete()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist or UnboundLocalError:
			return Response(status=status.HTTP_404_NOT_FOUND)


	def patch(self, request):
		try:
			id = request.data['id']
			patch_data = request.data['patch_data']
		except KeyError:
			Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			tmp_opinion = Opinion.objects.get(id=id)
			for new_data in patch_data.items():
				setattr(tmp_opinion, new_data[0],new_data[1])
				tmp_opinion.save()
			return Response(status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)