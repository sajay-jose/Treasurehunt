# Generated by Django 4.1.3 on 2023-04-16 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_user_game_alter_game_login_game_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='level',
            name='game',
        ),
    ]
