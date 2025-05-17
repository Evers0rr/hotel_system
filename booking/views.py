from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking, Profile
from .forms import BookingForm, CustomRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login


def is_available(room, start, end):
    return not Booking.objects.filter(
        room=room,
        start_time__lt=end,
        end_time__gt=start
    ).exists()

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('room_list')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/room_list.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    bookings = room.bookings.order_by('-start_time')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            if is_available(room, booking.start_time, booking.end_time):
                booking.save()
                messages.success(request, "Бронювання успішне!")
                return redirect('room_list')
            else:
                messages.error(request, "Цей час вже зайнято. Виберіть інший.")
    else:
        form = BookingForm()
    
    return render(request, 'booking/book_room.html', {'form': form, 'room': room, 'bookings': bookings})




