from .models import *
from rest_framework import serializers
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'phone_number']


class UserProfileListSerializer(serializers.ModelSerializer):
    followings_quantity = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'followings_quantity', 'email', 'age', 'phone_number']

    def get_followings_quantity(self, obj):
        return obj.get_followings_quantity()


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'profile_image', 'first_name', 'last_name']


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class MarketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['id', 'logo', 'market_name']


class MarketSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['logo', 'market_name']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['location']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['phone_number']


# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookListSerializer(serializers.ModelSerializer):
    market = MarketSimpleSerializer()

    class Meta:
        model = Book
        fields = ['id', 'book_image', 'book_name', 'price',
                  'age_restriction', 'market']


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    market = MarketSimpleSerializer()
    created_date = serializers.DateTimeField(format='%d %B %Y %H:%M')

    class Meta:
        model = Book
        fields = ['book_image', 'book_name', 'price', 'genre', 'pages',
                  'age_restriction', 'author', 'released_date', 'created_date', 'market']


class BookOwnEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class FavoriteItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer()
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True, source='book')

    class Meta:
        model = FavoriteItem
        fields = ['book', 'book_id']


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'favorite_items']


class MarketDetailSerializer(serializers.ModelSerializer):
    market_books = BookListSerializer(many=True, read_only=True)
    market_branches = BranchSerializer(many=True, read_only=True)
    market_contacts = ContactSerializer(many=True, read_only=True)
    followers_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Market
        fields = ['logo', 'market_name', 'followers_quantity', 'description', 'working_days',
                  'shift_start', 'shift_end', 'market_branches', 'market_contacts', 'market_books']

    def get_followers_quantity(self, obj):
        return obj.get_followers_quantity()


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    reset_code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')

        # Проверяем, существует ли указанный код для email
        try:
            token = ResetPasswordToken.objects.get(user__email=email, key=reset_code)
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Неверный код сброса или email.")

        data['user'] = token.user
        return data

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()
