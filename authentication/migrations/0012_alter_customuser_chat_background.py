# Generated by Django 5.0.6 on 2024-06-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_customuser_chat_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='chat_background',
            field=models.CharField(default='http://localhost:3000/static/backgrounds/default_chat_background.jpg', max_length=255),
        ),
    ]