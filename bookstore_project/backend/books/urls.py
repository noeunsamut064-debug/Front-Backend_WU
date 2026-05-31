from django.urls import path
from .views import (
    RegisterView, LoginView,
    CategoryListAPIView, BookListAPIView, BookDeleteAPIView,
    CartView, CartItemDetailView, CartClearView, CheckoutView,
)

urlpatterns = [
    path('api/register/',        RegisterView.as_view(),        name='register'),
    path('api/login/',           LoginView.as_view(),           name='login'),
    path('api/categories/',      CategoryListAPIView.as_view(), name='categories'),
    path('api/books/',           BookListAPIView.as_view(),     name='books'),
    path('api/books/<int:pk>/delete/',  BookDeleteAPIView.as_view(),   name='book-delete'),
    path('api/cart/',            CartView.as_view(),            name='cart'),
    path('api/cart/clear/',      CartClearView.as_view(),       name='cart-clear'),
    path('api/cart/checkout/',   CheckoutView.as_view(),        name='checkout'),
    path('api/cart/<int:pk>/',   CartItemDetailView.as_view(),  name='cart-item'),
]