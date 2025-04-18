# Generated by Django 5.1.6 on 2025-03-08 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_market', '0002_delete_author_rename_image_market_logo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='genre_name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='genre_name_ky',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='genre_name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='description_ky',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='description_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='market_name_en',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='market_name_ky',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='market',
            name='market_name_ru',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
