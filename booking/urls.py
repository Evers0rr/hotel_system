from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('booking/<int:room_id>/', views.book_room, name='book_room'),
]



