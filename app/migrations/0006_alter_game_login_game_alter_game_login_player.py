# Generated by Django 4.1.3 on 2023-04-16 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_game_login_joined_at_user_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game_login',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.game'),
        ),
        migrations.AlterField(
            model_name='game_login',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
