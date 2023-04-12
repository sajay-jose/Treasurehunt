from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from .models import User,Game
from .forms import EditplayerForm, EditProfileForm, EditgameForm,EditlevelForm,ViewgameForm
from .decorator import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages



# Create your views here.

def home(request):
    return render(request,'login.html')
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        print('email:', email)
        register_as = request.POST['register_as']
        print('register_as:', register_as)
        phonecode = request.POST['phonecode']
        phone = request.POST['phone']
        password = request.POST['password']
        print('password:', password)
        if register_as == '1': #coordinator
            game_name = request.POST['game_name']
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, phonecode=phonecode, phone=phone, )
            user.save()
            game = Game.objects.create(game_name=game_name, game_email=email)
            game.save()
        elif register_as == '2': #player
            game_id = request.POST['game_id']
            game = Game.objects.get(game_id=game_id)
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, phonecode=phonecode, phone=phone, game=game)
            user.save()
            print('user:', user)
        return redirect(register_sucess)


def register_sucess(request):
    return render(request,'register_sucess.html')

def my_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        # register_as = request.POST.get('register_as')
        if email and password:
            # User = get_user_model()
            try:
                user = User.objects.get(email=email, password=password)
                if check_password(password, user.password):
                    # user = authenticate(request, email=email, password=password)
                    # user = User.objects.get(email=email)
                    print(user)
                # if check_password(password, user.password):
                if user is not None:
                    register_as = user.register_as
                    if user.register_as == 2 and int(register_as) == 2:   #player
                        login(request, user)
                        request.session['email'] = email
                        return redirect('player_dashboard')
                    elif user.register_as == 1 and int(register_as) == 1:  #coordinator
                        login(request, user)
                        request.session['email'] = email
                        return redirect('coordinator_dashboard')
                    else:
                        return HttpResponse("Invalid user type")
                else:
                    return HttpResponse("Invalid login credentials")
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}")
        else:
            return HttpResponse("Email and password are required.")
    else:
        return render(request, 'login.html')

def my_logout(request):
    logout(request)
    return redirect(my_login)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'edit_profile.html', {'form': form})

def player_dashboard(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    context = {'user': user}
    return render(request, 'player-dashboard/app.html', context)

def coordinator_dashboard(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    games = Game.objects.get(game_email=email)
    users = games.players.all()
    game = user.games_created.all()
    context = {'users': users, 'game': game, 'user': user}
    return render(request, 'coordinator-dashboard/app.html', context)


def send_test_email(request):
    send_mail(
        'Test email',
        'This is a test email.',
        settings.EMAIL_HOST_USER,
        ['sajayjose24@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Email sent successfully.')



def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse('Email does not exist')

        # Generate a password reset token
        token = user.generate_password_reset_token()
        context = {
            'uid': user.uid,
            'email': user.email,
            'name': user.name,
            'token': token,
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
        }
        subject = 'Password reset'
        message = 'Please click on the following link to reset your password: {protocol}://{domain}/reset/{uid}/{token}'.format(
            **context)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        return HttpResponse('Password reset email sent')

    return render(request, 'login.html')

def password(request, uid, token):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        # Check if the new password and confirm password match
        if new_password != confirm_password:
            return HttpResponse("Passwords don't match")
        # Authenticate the user with the current password
        user = authenticate(email=email, password=password)
        if user is not None:
            # Hash the new password and update the user object
            user.password = make_password(new_password)
            user.save()
            # Redirect the user to the login page
            return redirect('login')
        else:
            # Return an error message if authentication fails
            return HttpResponse("Invalid current password")
    else:
        user = get_object_or_404(User, uid=uid)
        if user.is_password_reset_token_valid(token):
            # Token is valid, allow user to reset password
            return render(request, 'change_password.html')
        else:
            # Token is invalid, show error message
            return HttpResponse("Invalid password reset link")

  # if request.method == 'POST':
  #   email = request.POST['email']
  #   password = request.POST['password']
  #   new_password = request.POST['new_password']
  #   confirm_password = request.POST['confirm_password']
  #   # Check if the new password and confirm password match
  #   if new_password != confirm_password:
  #       return HttpResponse(" password don't match")
  #   # Authenticate the user with the current password
  #   user = authenticate(email=email, password=password)
  #   if user is not None:
  #       # Hash the new password and update the user object
  #       user.password = make_password(new_password)
  #       user.save()
  #       # Redirect the user to the login page
  #       return redirect('login.html')
  #   else:
  #       # Return an error message if authentication fails
  #       return HttpResponse("Invalid current password")
  # else:
  #     return render(request, 'change_password.html')


def change_password(request):
    return render(request, 'change_password.html')

def player_game_details(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    games = Game.objects.get(game_email=email)
    game = Game.objects.filter(creater=user).all()
    context = {'game': game}
    return render(request, 'player-dashboard/player_game_details.html', context)

def scoreboard(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'player-dashboard/scoreboard.html', context)

def player_details(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    games = Game.objects.filter(creater=user)
    game_players = {}
    for game in games:
        players = User.objects.filter(game=game)
        game_players[game] = players
    context = {'game_players': game_players, 'user': user}
    return render(request, 'coordinator-dashboard/player_details.html', context)


def game_create(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    users = User.objects.all()
    if request.method == 'POST':
        game_name = request.POST.get('game_name')
        game_id = request.POST.get('game_id')
        clues = request.POST.get('clues')
        game_level = request.POST.get('game_level')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        rules = request.POST.get('rules')
        game = Game.objects.create(
                game_name=game_name,
                game_id=game_id,
                clues=clues,
                game_level=game_level,
                start_date=start_date,
                end_date=end_date,
                rules=rules
            )
        return HttpResponse("Game Created")
    context = {'user': user}
    return render(request, 'coordinator-dashboard/game_create.html', context)

def coordinator_game_detail(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    game = Game.objects.get(game_email=email)
    # games = Game.objects.filter(coordinator=user).all()
    games = Game.objects.filter(game_email=email)
    context = {'games': games , 'game': game, 'user': user}
    return render(request, 'coordinator-dashboard/coordinator_game_detail.html', context)



def edit_player(request,uid):
    player = User.objects.get(uid=uid)
    form = EditplayerForm(instance=player)
    if request.method == 'POST':
        form = EditplayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_details')
    context = {'form': form, 'player': player}
    return render(request, 'coordinator-dashboard/edit_player.html', context)

def delete_player(request,uid):
    player = User.objects.get(uid=uid)
    player.delete()
    return redirect('player_details')

def analytics(request):
    email = request.session['email']
    user = User.objects.get(email=email)
    users = User.objects.all()
    # Get the total number of players registered
    print(User.objects.filter(register_as='2', email=email))
    num_players = User.objects.filter(register_as='2', email=email).count()

    context = {'num_players': num_players, 'user': user}

    return render(request, 'coordinator-dashboard/analytics.html', context)

def edit_game(request,id):
    email = request.session['email']
    user = User.objects.get(email=email)
    game = Game.objects.get(pk=id)
    form = EditgameForm(instance=game)
    if request.method == 'POST':
        form = EditgameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('coordinator_game_detail')
    context = {'form': form, 'game': game, 'user': user}
    return render(request, 'coordinator-dashboard/edit_game.html', context)

def view_game(request, id):
    email = request.session['email']
    user = User.objects.get(email=email)
    game = Game.objects.get(pk=id)
    form = ViewgameForm(instance=game)
    if request.method == 'POST':
        form = ViewgameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('edit_level')
    context = {'form': form, 'game': game, 'user': user}
    return render(request, 'coordinator-dashboard/view_game.html', context)

def delete_game(request,id):
    game = Game.objects.get(pk=id)
    game.delete()
    return redirect('coordinator_game_detail')

def edit_level(request,id):
    email = request.session['email']
    user = User.objects.get(email=email)
    game = Game.objects.get(pk=id)
    form = EditlevelForm(instance=game)
    if request.method == 'POST':
        form = EditlevelForm(request.POST, instance=game)
        if form.is_valid():
            form.cleaned_data['password_result'] = 'password_result'
            form.save()
            return redirect('coordinator_game_detail')
    context = {'form': form, 'game': game, 'user': user}
    return render(request, 'coordinator-dashboard/edit_level.html', context)

