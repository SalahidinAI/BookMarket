from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import viewsets, generics
from .permissions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyResetCodeSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserEdit]


class MarketAPIView(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketCreateAPIView(generics.CreateAPIView):
    serializer_class = MarketSerializer


class MarketListAPIView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketListSerializer


class MarketDetailAPIView(generics.RetrieveAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketDetailSerializer


class MarketOwnAPIView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketDetailSerializer

    def get_queryset(self):
        return Market.objects.filter(owner=self.request.user)


class MarketEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    permission_classes = [MarketOwnEdit]


class BranchCreateAPIView(generics.CreateAPIView):
    serializer_class = BranchSerializer


class BranchEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [BranchContactEdit]


class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactSerializer


class ContactEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [BranchContactEdit]


class SubscriptionUserListAPIView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketListSerializer

    def get_queryset(self):
        return Market.objects.filter(market_subscriptions__user=self.request.user)


class SubscriptionUserDetailAPIView(generics.RetrieveAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketDetailSerializer
    # permission_classes = # if need


class SubscriptionMarketAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer

    def get_queryset(self):
        market_id = self.kwargs.get("market_id")
        return UserProfile.objects.filter(user_subscriptions__market_id=market_id)


# class SubscriptionMarketDetailAPIView(generics.RetrieveAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer


class BookCreateAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookOwnEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookOwnEditSerializer
    permission_classes = [BookOwnEdit]


class GenreAPIView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FavoriteAPIView(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializers = self.get_serializer(favorite)
        return Response(serializers.data)


class FavoriteItemAPIView(viewsets.ModelViewSet):
    serializer_class = FavoriteItemSerializer

    def get_queryset(self):
        return FavoriteItem.objects.filter(favorite__user=self.request.user)

    def perform_create(self, serializer):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer.save(favorite=favorite)


@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def toggle_follow(request, market_id):
    try:
        market = Market.objects.get(id=market_id)
    except Market.DoesNotExist:
        return Response({'detail': 'Market not found'}, status=status.HTTP_404_NOT_FOUND)

    subscription, created = Subscription.objects.get_or_create(user=request.user, market=market)

    if not created:
        subscription.delete()
        return Response({'detail': 'Subscription deleted'}, status=status.HTTP_200_OK)

    return Response({'detail': 'Subscription created'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def toggle_book_like(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    like, created = Like.objects.get_or_create(user=request.user, book=book)

    if not created:
        like.delete()
        return Response({'detail': 'Like deleted'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'detail': 'Like created'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def toggle_comment_like(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except CommentLike.DoesNotExist:
        return Response({'detail': 'Comment_like not found'}, status=status.HTTP_404_NOT_FOUND)

    comment_like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

    if not created:
        comment_like.delete()
        return Response({'detail': 'Comment_like deleted'}, status=status.HTTP_200_OK)

    return Response({'detail': 'Comment_like created'}, status=status.HTTP_201_CREATED)

