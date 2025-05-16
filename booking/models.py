from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

        

class Room(models.Model):
    name =  models.CharField(max_length=50) 
    capacity = models.IntegerField()
    description = models.TextField(blank=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,blank=False,related_name='rooms')
    features = models.CharField(max_length=255, blank=False)
    price_for_hour = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Кімнати'
        verbose_name = 'Кімнату'

    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.EmailField(blank=False)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'
  
    def __str__(self):
        return f'Юзер: {self.user.username}'
    
    

class Booking(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,related_name='bookings')
    room = models.ForeignKey('Room', on_delete=models.CASCADE,related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_time']
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"
        unique_together = ('room', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.room.name} | {self.start_time.strftime('%Y-%m-%d %H:%M')} — Забронював кімнату:{self.user.username}"
    # %Y - рік
    # %m - місяць
    # %d - день
    # %H - година
    # %M - хвилина
    


    
        
    