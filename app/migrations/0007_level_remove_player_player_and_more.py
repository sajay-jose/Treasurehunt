# Generated by Django 4.1.3 on 2023-04-12 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_user_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('game_level', models.CharField(max_length=1)),
                ('clues', models.CharField(max_length=500)),
                ('rules', models.TextField()),
                ('password_result', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
                ('answer', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='player',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='coordinator',
            new_name='creater',
        ),
        migrations.RemoveField(
            model_name='game',
            name='clues',
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_level',
        ),
        migrations.RemoveField(
            model_name='game',
            name='password',
        ),
        migrations.RemoveField(
            model_name='game',
            name='password_result',
        ),
        migrations.RemoveField(
            model_name='game',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='user',
            name='game',
        ),
        migrations.DeleteModel(
            name='Coordinator',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.AddField(
            model_name='level',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='games', to='app.game'),
        ),
    ]