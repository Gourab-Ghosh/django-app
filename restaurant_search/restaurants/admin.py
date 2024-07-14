from django.contrib import admin
from .models import Restaurant, Dish

class DishInline(admin.TabularInline):
    model = Dish
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [DishInline]
    list_display = ('name', 'location')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Dish)
