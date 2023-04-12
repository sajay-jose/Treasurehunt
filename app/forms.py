from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from.models import User,Game,Level
from django import forms

class EditplayerForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
        ]

class EditgameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['game_name', 'game_id']

class ViewgameForm(ModelForm):
    class Meta:
        model = Level
        fields = ['game_level']

TYPE_CHOICES = (
    ('password_result', 'password_result'),
)
class EditlevelForm(ModelForm):
    password_result = forms.ChoiceField(choices=TYPE_CHOICES, required=True)
    class Meta:
        model = Level
        fields = ['password_result', 'clues', 'password']