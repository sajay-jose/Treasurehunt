from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from.models import User, Game


class EditplayerForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['name', 'email']

class EditgameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['game_name', 'game_id', 'rules']


