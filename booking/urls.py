from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import register, profile, login_view, initiate_booking, confirm_booking

urlpatterns = [
    path('', views.home, name='home'),
    path('rooms/',views.room_list, name='room_list'),
    path('booking/<int:room_id>/', views.book_room, name='book_room'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('booking/<int:room_id>/rate/', views.rate_room, name='rate_room'),
    path('booking/<int:room_id>/start/', views.initiate_booking, name='initiate_booking'),
    path('booking/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/confirm/', views.confirm_booking, name='confirm_booking'),
]



