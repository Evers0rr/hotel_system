from django.shortcuts import render
from .models import Room
# Create your views here.


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})

def book_room(request, room_id):
    return render(request, 'booking/book_room.html', {'room_id': room_id})


