# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, generics
# from .models import Book, Category, CartItem
# from .serializers import BookSerializer, CategorySerializer, CartItemSerializer


# class CategoryListAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class BookListAPIView(generics.ListAPIView):
#     serializer_class = BookSerializer

#     def get_queryset(self):
#         queryset = Book.objects.all()
#         category = self.request.query_params.get('category')
#         search = self.request.query_params.get('search')
#         if category:
#             queryset = queryset.filter(category__id=category)
#         if search:
#             queryset = queryset.filter(title__icontains=search)
#         return queryset


# class BookDeleteAPIView(APIView):
    def delete(self, request, pk):
#         try:
#             book = Book.objects.get(id=pk)
#             book.delete()
#             return Response({'message': f'"{book.title}" deleted!'}, status=status.HTTP_200_OK)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


class CartClearView(APIView):
    def delete(self, request):
        items = CartItem.objects.select_related('book').all()
        for item in items:
            item.book.stock += item.quantity
            item.book.save()
        items.delete()
        return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


# class CartView(APIView):

#     def get(self, request):
#         items = CartItem.objects.select_related('book').all()
#         serializer = CartItemSerializer(items, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         book_id = request.data.get('book')
#         quantity = request.data.get('quantity', 1)
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#         if book.stock < quantity:
#             return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

#         cart_item, created = CartItem.objects.get_or_create(book=book)
#         if not created:
#             cart_item.quantity += quantity
#         else:
#             cart_item.quantity = quantity
#         cart_item.save()

#         book.stock -= quantity
#         book.save()

#         return Response({
#             'message': f'"{book.title}" added to cart!',
#             'book_id': book.id,
#             'quantity': cart_item.quantity,
#             'remaining_stock': book.stock
#         }, status=status.HTTP_200_OK)

#     def delete(self, request):
#         CartItem.objects.all().delete()
#         return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


# class CartItemDetailView(APIView):

#     def patch(self, request, pk):
#         try:
#             item = CartItem.objects.get(id=pk)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
#         item.quantity = request.data.get('quantity', item.quantity)
#         item.save()
#         return Response({'message': 'Quantity updated.'}, status=status.HTTP_200_OK)

#     def delete(self, request, pk):
#         try:
#             item = CartItem.objects.get(id=pk)
#             item.delete()
#             return Response({'message': 'Item removed.'}, status=status.HTTP_200_OK)
#         except CartItem.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


# class CartClearView(APIView):
#     def delete(self, request):
#         CartItem.objects.all().delete()
#         return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


# class CheckoutView(APIView):
#     def post(self, request):
#         items = CartItem.objects.all()
#         if not items.exists():
#             return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
#         items.delete()
#         return Response({'message': 'Order placed successfully!'}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, get_user_model
from .models import Book, Category, CartItem, Order, OrderItem
from .serializers import (
    BookSerializer, CategorySerializer, CartItemSerializer,
    RegisterSerializer, LoginSerializer
)

User = get_user_model()


# AUTH
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful!', 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'message': 'Login successful!',
            'user': {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}
        }, status=status.HTTP_200_OK)


# BOOKS
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        if category:
            queryset = queryset.filter(category__id=category)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset


class BookDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response({'message': f'"{book.title}" deleted!'}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)


# class CartClearView(APIView):
#     def delete(self, request):
#         items = CartItem.objects.select_related('book').all()
#         for item in items:
#             item.book.stock += item.quantity
#             item.book.save()
#         items.delete()
#         return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


# CART
class CartView(APIView):

    def get(self, request):
        items = CartItem.objects.select_related('book').all()
        serializer = CartItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        book_id = request.data.get('book')
        quantity = request.data.get('quantity', 1)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        if book.stock < quantity:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
        cart_item, created = CartItem.objects.get_or_create(book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        book.stock -= quantity
        book.save()
        return Response({'message': f'"{book.title}" added to cart!'}, status=status.HTTP_200_OK)

    def delete(self, request):
        items = CartItem.objects.select_related('book').all()
        for item in items:
            item.book.stock += item.quantity
            item.book.save()
        items.delete()
        return Response({'message': 'Cart cleared.'}, status=status.HTTP_200_OK)


class CartItemDetailView(APIView):

    def patch(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        new_quantity = request.data.get('quantity', item.quantity)
        diff = new_quantity - item.quantity

        if diff > 0 and item.book.stock < diff:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        item.book.stock -= diff
        item.book.save()
        item.quantity = new_quantity
        item.save()
        return Response({'message': 'Quantity updated.'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk)
            item.book.stock += item.quantity
            item.book.save()
            item.delete()
            return Response({'message': 'Item removed.'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


# CHECKOUT
class CheckoutView(APIView):

    def post(self, request):
        cart_items = CartItem.objects.all()
        if not cart_items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.book.price * item.quantity for item in cart_items)
        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, total_price=total_price, status='pending')
            OrderItem.objects.bulk_create([
                OrderItem(order=order, book=item.book, quantity=item.quantity, price=item.book.price)
                for item in cart_items
            ])
            order_id = order.id
        else:
            order_id = None

        cart_items.delete()
        response_data = {'message': 'Order placed successfully!'}
        if order_id is not None:
            response_data['order_id'] = order_id
        return Response(response_data, status=status.HTTP_201_CREATED)