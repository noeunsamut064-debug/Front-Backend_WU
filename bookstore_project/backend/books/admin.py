# books/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, Category, CartItem, OrderItem, Order, User

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'price', 'stock', 'category']
    list_filter = ['category']
    search_fields = ['title', 'author']
    list_per_page = 20

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'quantity', 'added_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_price', 'status']
    list_filter = ['status']
    search_fields = ['user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'book', 'quantity', 'price']

admin.site.register(User, UserAdmin)
