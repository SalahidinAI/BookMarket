from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class UserProfileAPIView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class MarketAPIView(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class BranchAPIView(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class ContactAPIView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# class EventAPIView(viewsets.ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer


class SubscriptionAPIView(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer




class BookAPIView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class =BookSerializer



class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        book = Book.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=book)

        if not created:
            like.delete()
            return Response({"message": "Лайк удален"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Лайк добавлен"}, status=status.HTTP_201_CREATED)


# class AuthorAPIView(viewsets.ModelViewSet):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer


class GenreAPIView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class FavoriteAPIView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemAPIView(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer


class LikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def book(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Комментарий не найден"}, status=status.HTTP_404_NOT_FOUND)

        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)

        if not created:
            like.delete()
            return Response({"message": "Лайк удален"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Лайк добавлен"}, status=status.HTTP_201_CREATED)

