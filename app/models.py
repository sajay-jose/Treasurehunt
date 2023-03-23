from django.db import models
from django.contrib.auth.hashers import make_password
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.crypto import get_random_string
import hashlib
# Create your models here.




class User(models.Model):
    REGISTER_CHOICES = (
        ('1', 'Coordinator'),
        ('2', 'Player'),
    )
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    new_password = models.CharField(max_length=128,null=True,blank=True)
    register_as = models.IntegerField(choices=REGISTER_CHOICES, null=False, blank=False)
    game_name = models.CharField(max_length=50, blank=True, null=True)
    game_id = models.CharField(max_length=20, blank=True, null=True)
    phonecode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    token = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # def delete(self, *args, **kwargs):
    #     self.deleted = True
    #     self.save()
    #
    # def hard_delete(self, *args, **kwargs):
    #     super(User, self).delete(*args, **kwargs)

    def generate_password_reset_token(self):
        # Generate a random string
        random_string = get_random_string(length=32)
        # Generate a hash of the random string
        token_hash = hashlib.sha256(random_string.encode('utf-8')).hexdigest()
        # Set the token hash to the user's token field
        self.token = token_hash
        self.save()
        # Return the random string as the password reset token
        return random_string

    def is_password_reset_token_valid(self, token):
        if self.token != token:
            return False

        expiration_time = datetime.now() - timedelta(hours=settings.PASSWORD_RESET_TIMEOUT_HOURS)
        if self.date_joined < expiration_time:
            return False
        return True

class Game(models.Model):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )

    game_name = models.CharField(max_length=50)
    game_id = models.CharField(max_length=50, unique=True)
    game_level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    clues = models.CharField(max_length=500)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    rules = models.TextField()

    def __str__(self):
        return self.game_name
