from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from django.utils import timezone

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