from django.contrib import admin
from .models import Category, Room, Booking, Profile, Post, RoomRating
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'capacity', 'price_for_hour')
    search_fields = ('name', 'features', 'category__name')
    list_filter = ('category', 'capacity')
    ordering = ('name',)
    autocomplete_fields = ('category',)
    fieldsets = (
        (None, {'fields': ('name', 'category', 'capacity')}),
        ('Деталі', {'fields': ('description', 'features', 'price_for_hour')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'address')
    ordering = ('user__username',)
    autocomplete_fields = ('user',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'start_time', 'end_time', 'is_confirmed')
    search_fields = ('user__username', 'room__name')
    list_filter = ('is_confirmed', 'start_time')
    ordering = ('-start_time',)
    autocomplete_fields = ('user', 'room')
    actions = ['mark_as_confirmed']

    @admin.action(description="Позначити як підтверджене")
    def mark_as_confirmed(self, request, queryset):
        queryset.update(is_confirmed=True)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


@admin.register(RoomRating)
class RoomRatingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'rating')
    list_filter = ('rating',)
    search_fields = ('room__name', 'user__username')
    autocomplete_fields = ('room', 'user')
    ordering = ('-rating',)

