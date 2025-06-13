from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking,Post, RoomRating, BookingConfirmation
from .forms import BookingForm, CustomRegisterForm, RatingForm, ConfirmCodeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Avg, Q
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
import uuid


def is_available(room, start, end):
    return not Booking.objects.filter(
        room=room,
        start_time__lt=end,
        end_time__gt=start
    ).exists()

def home(request):
    post_list = Post.objects.order_by('-created_at')
    return render(request, 'based/home.html',{'news_list': post_list})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'👋 Вітаємо, {user.username}!')
            return redirect('profile')  
        else:
            messages.error(request, '❌ Невірне імʼя користувача або пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('room').order_by('-start_time')
    ratings = RoomRating.objects.filter(user=request.user).select_related('room')
    return render(request, 'users/profile.html', {
        'bookings': user_bookings,
        'user': request.user,
        'ratings': ratings,
    })

def room_list(request):
    rooms = Room.objects.annotate(avg_rating=Avg('roomrating__rating'))
    return render(request, 'booking/room_list.html', {'rooms': rooms})

def initiate_booking(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if not request.user.is_authenticated:
        messages.warning(request, '🔒 Щоб бронювати кімнату, спочатку увійдіть.')
        return redirect(f"{settings.LOGIN_URL}?next=/booking/{room_id}/")

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            if Booking.objects.filter(
                room=room,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists():
                messages.error(request, '❌ Ця кімната вже заброньована у вибраний період.')
                return redirect("book_room", room_id=room.id)

            confirmation = BookingConfirmation.objects.create(
                user=request.user,
                room=room,
                start_time=start_time,
                end_time=end_time,
            )

            send_mail(
                subject="Підтвердження бронювання кімнати",
                message=(
                    f"Привіт! Це автоматичний лист з сайту по бронюванню кімнат у Готелі.\n"
                    f"Ви намагалися забронювати кімнату: {room.name}\n"
                    f"Введіть цей код на нашому сайті: {confirmation.code}\n"
                    f"Якщо ви нічого не бронювали — просто проігноруйте цей лист."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            return redirect('confirm_booking')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

            return redirect("book_room", room_id=room.id)

    return redirect("book_room", room_id=room.id)

@login_required
def confirm_booking(request):
    if request.method == 'POST':
        form = ConfirmCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                confirmation = BookingConfirmation.objects.get(code=code)
            except BookingConfirmation.DoesNotExist:
                messages.error(request, '❌ Невірний код підтвердження.')
            else:
                if confirmation.user != request.user:
                    messages.error(request, '❌ Ви не можете підтвердити це бронювання.')
                else:
                    Booking.objects.create(
                        user=confirmation.user,
                        room=confirmation.room,
                        start_time=confirmation.start_time,
                        end_time=confirmation.end_time,
                    )
                    messages.success(request, '✅ Бронювання підтверджено.')
                    confirmation.delete()
                    return redirect('profile')
    else:
        form = ConfirmCodeForm()

    return render(request, 'booking/confirm_booking.html', {'form': form})

def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    bookings = Booking.objects.filter(room=room).order_by('-start_time')
    average_rating = RoomRating.objects.filter(room=room).aggregate(avg=Avg('rating'))['avg']

    booking_form = BookingForm()
    rating_form = RatingForm()

    if not request.user.is_authenticated:
        messages.warning(request, '🔒 Для того щоб забронювати кімнату, потрібно увійти або зареєструватися.')
        return redirect(f"{settings.LOGIN_URL}?next=/booking/{room_id}/")

    if request.method == 'POST':
        if 'submit_rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                existing_rating = RoomRating.objects.filter(user=request.user, room=room).first()
                if existing_rating:
                    existing_rating.rating = rating_form.cleaned_data['rating']
                    existing_rating.save()
                    messages.success(request, '✅ Оцінку оновлено.')
                else:
                    new_rating = rating_form.save(commit=False)
                    new_rating.user = request.user
                    new_rating.room = room
                    new_rating.save()
                    messages.success(request, '✅ Оцінку додано.')
                return redirect('book_room', room_id=room.id)

    return render(request, 'booking/book_room.html', {
        'room': room,
        'form': booking_form,
        'rating_form': rating_form,
        'bookings': bookings,
        'average_rating': average_rating,
        'range': range(1, 6),
    })

def rate_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    rating, created = RoomRating.objects.get_or_create(user=request.user, room=room)

    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Вашу оцінку збережено!')
            return redirect('room_detail', room_id=room.id)
    else:
        form = RatingForm(instance=rating)

    return render(request, 'booking/rate_room.html', {
        'room': room,
        'form': form,
    })







