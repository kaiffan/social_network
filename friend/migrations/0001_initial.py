# Generated by Django 5.0.6 on 2024-06-07 19:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendship_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACCEPTED', 'accepted'), ('PENDING', 'pending'), ('REJECTED', 'rejected'), ('DELETED', 'deleted')])),
                ('friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_friend_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_friend_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'friend',
                'unique_together': {('user_id', 'friend_id')},
            },
        ),
    ]
