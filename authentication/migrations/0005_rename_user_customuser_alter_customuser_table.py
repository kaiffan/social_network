# Generated by Django 5.0.6 on 2024-06-04 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authentication', '0004_user_delete_customuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='CustomUser',
        ),
        migrations.AlterModelTable(
            name='customuser',
            table='custom_user',
        ),
    ]
