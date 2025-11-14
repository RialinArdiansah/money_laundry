from django.contrib import admin
from .models import User, Customer, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'phone', 'position')
    list_filter = ('role',)
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'service_type', 'weight_kg', 'total_cost', 'status')
    list_filter = ('service_type', 'status')
    search_fields = ('order_number', 'customer__name')