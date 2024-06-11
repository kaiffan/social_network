# Generated by Django 5.0.6 on 2024-06-11 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('message', '0007_delete_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='attachments')),
                ('attachment_type', models.TextField(choices=[('FILE', 'file'), ('IMAGE', 'image'), ('VIDEO', 'video')])),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.message')),
            ],
            options={
                'db_table': 'attachment',
            },
        ),
    ]
