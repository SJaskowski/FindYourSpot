from django.contrib import admin
from .models import Custom_User, Apartment, Room, Address, Images, Opinion

# Register your models here.

admin.site.register(Custom_User)
admin.site.register(Apartment)
admin.site.register(Address)
admin.site.register(Images)
admin.site.register(Opinion)
admin.site.register(Room)
