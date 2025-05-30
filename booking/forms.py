from django import forms
from .models import Booking, RoomRating
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields =  ['start_time','end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end:
            if end <= start:
                raise ValidationError("Кінцева дата має бути пізніше за початкову.")

            if start < timezone.now():
                raise ValidationError("Неможливо забронювати в минулому.")
            
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError(_("Пароль повинен містити щонайменше 8 символів."))
        if password.isdigit():
            raise ValidationError(_("Пароль не може складатися лише з цифр."))
        return password
       
class RatingForm(forms.ModelForm):
    class Meta:
        model = RoomRating
        fields = ['rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
        }