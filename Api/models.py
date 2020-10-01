from datetime import datetime
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.text import slugify
from pip._internal.utils.misc import enum


class Role(Enum):
	customer = 1
	owner = 2
	admin = 3


class Custom_User(AbstractUser):
	role = models.CharField(max_length=10, blank=True)


def get_image_filename(instance, filename):
	title = instance.room.name
	slug = slugify(title)
	return "post_images/%s-%s" % (slug, filename)


class Apartment(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(max_length=1000, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	owner = models.ForeignKey(Custom_User, default=None, on_delete=models.CASCADE, blank=True, null=True)
	rented = models.BooleanField(default=False, null=True, blank=True)


class Room(models.Model):
	name = models.CharField(max_length=50)
	apartment = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, blank=True, null=True)
	description = models.TextField(max_length=1000, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	area_metrage = models.FloatField(blank=True, null=True)
	rented = models.BooleanField(default=False, null=True, blank=True)


class Images(models.Model):
	room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(upload_to=get_image_filename,
	                          verbose_name='Image')


class Address(models.Model):
	apartment = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, blank=True)
	street_name = models.CharField(max_length=100)
	house_nr = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=6)
	city = models.CharField(max_length=100)


class Opinion(models.Model):
	room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE)
	apartment = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, blank=True, null=True)
	description = models.TextField(max_length=1000, blank=True)
	poster = models.ForeignKey(Custom_User, default=None, on_delete=models.CASCADE)


class Advert(models.Model):
	room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE, blank=True, null=True)
	apartment = models.ForeignKey(Apartment, default=None, on_delete=models.CASCADE, blank=True, null=True)
	posting_date = models.DateField(default=datetime.now())
	active = models.BooleanField(default=True)
	ended_on = models.DateField(blank=True, null=True)
	pass
