
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book, Category, CartItem, Order, OrderItem

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'customer'),
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'price', 'stock', 'image', 'category', 'category_name']

class CartItemSerializer(serializers.ModelSerializer):
    book_title    = serializers.CharField(source='book.title', read_only=True)
    book_author   = serializers.CharField(source='book.author', read_only=True)
    book_price    = serializers.FloatField(source='book.price', read_only=True)
    book_image    = serializers.ImageField(source='book.image', read_only=True)
    book_category = serializers.CharField(source='book.category.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_title', 'book_author', 'book_price', 'book_image', 'book_category', 'quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'total_price', 'status', 'items']