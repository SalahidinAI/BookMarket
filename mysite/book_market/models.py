from datetime import datetime
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(110)],
        null=True, blank=True
    )
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f'{self.field} - {self.last_name}'


class Market(models.Model):
    logo = models.ImageField(upload_to='market_images/')
    market_name = models.CharField(max_length=64)
    description = models.TextField()
    WORKING_DAYS = (
        ('ПН', 'ПН'),
        ('ВТ', 'ВТ'),
        ('СР', 'СР'),
        ('ЧТ', 'ЧТ'),
        ('ПТ', 'ПТ'),
        ('СБ', 'СБ'),
        ('ВС', 'ВС'),
    )
    working_days = MultiSelectField(choices=WORKING_DAYS, max_choices=7, max_length=32)
    # добавь 24 часа
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return f'{self.market_name}'


class Branch(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.market} branch'


class Contact(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'{self.market} contact'

    class Meta:
        unique_together = ('market', 'phone_number')


class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} --> {self.market}'

    class Meta:
        unique_together = ('user', 'market')


class Genre(models.Model):
    genre_name = models.CharField(max_length=64)

    def __str__(self):
        return self.genre_name


class Book(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=64)
    book_image= models.ImageField(upload_to='book_images/')
    price = models.PositiveSmallIntegerField()
    genre = models.ManyToManyField(Genre)
    current_year = datetime.now().year
    released_date = models.PositiveSmallIntegerField(validators=[
        MaxValueValidator(current_year)
    ])
    pages = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(3), MaxValueValidator(5000)
    ])
    AGE_CHOICES = (
        ('детский', 'детский'),
        ('взрослый', 'взрослый'),
    )
    author = models.CharField(max_length=120)
    age_restriction = models.CharField(choices=AGE_CHOICES, max_length=16)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.book_name} {self.market}'


class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'user: {self.user} --> {self.book}'

    class Meta:
        unique_together = ('user', 'book')


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} --> {self.book}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        unique_together = ('user', 'comment')


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'favorite: {self.favorite}, {self.book}'

    class Meta:
        unique_together = ('favorite', 'book')
