# Generated by Django 5.0.6 on 2024-06-10 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialogue', '0006_alter_dialogue_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dialogue',
            name='is_chat',
        ),
    ]
