from django.contrib import admin
from .models import Category, Room, Booking, Profile, Post, RoomRating
# Register your models here.

admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(RoomRating)
