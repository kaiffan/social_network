# Generated by Django 5.0.6 on 2024-06-10 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='theme',
            field=models.BooleanField(default=False, max_length=255, verbose_name='theme'),
        ),
    ]
