# Generated by Django 5.1.4 on 2025-01-08 02:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0005_alter_book_category_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Romance', 'Romance'), ('technelogy', 'technelogy'), ('Mystery', 'Mystery')], max_length=190, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Delivered', 'Delivered'), ('out of order', 'out of order'), ('in progress', 'in progress')], max_length=200, null=True),
        ),
    ]
