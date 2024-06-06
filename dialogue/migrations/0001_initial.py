# Generated by Django 5.0.6 on 2024-06-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('is_chat', models.BooleanField(default=True)),
                ('is_dialogue', models.BooleanField(default=False)),
            ],
        ),
    ]