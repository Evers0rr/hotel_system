from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import BookingForm
# Create your views here.


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})

def book_room(request, room_id):
    room = get_object_or_404(Room, id = room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()
            return redirect('room_list')
    else:
        form = BookingForm()
    
    return render(request, 'booking/book_room.html', {'form': form, 'room':room})


