from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Game, Level, Game_login
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
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, phonecode=phonecode, phone=phone,)
            user.save()
            # game = Game.objects.create(creater_id=user.uid)
            # game.save()
        elif register_as == '2': #player
            # game_id = request.POST['game_id']
            # game = Game.objects.get(game_id=game_id)
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, phonecode=phonecode, phone=phone,)
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
                        request.session['uid'] = user.uid
                        if Game_login.objects.filter(player=user).exists():
                            return redirect('player_dashboard')
                        else:
                            return redirect('player_home')
                    elif user.register_as == 1 and int(register_as) == 1:  #coordinator
                        login(request, user)
                        request.session['uid'] = user.uid
                        if Game.objects.filter(creater=user).exists():
                            return redirect('coordinator_dashboard')
                        else:
                            return redirect('game_create')
                    else:
                        return HttpResponse("Invalid user type")
                else:
                    return HttpResponse("Invalid login credentials")
            except Exception:
                messages.success(request, "email and password doesn't match")
                return render(request, 'login.html')
        else:
            return HttpResponse("Email and password are required.")
    else:
        return render(request, 'login.html')

def my_logout(request):
    logout(request)
    return redirect(my_login)

def change_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        # Check if the new password and confirm password match
        if new_password != confirm_password:
            return HttpResponse("Passwords don't match")
        # Retrieve the user object based on email
        user = User.objects.filter(email=email).first()
        print(user)
        if user is not None:
            # Hash the new password and update the user object
            user.password = new_password
            user.save()
            # Redirect the user to the login page
            return redirect('login')
    return render(request, 'change_password.html')

def edit_profile(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('coordinator_dashboard')
        else:
            form = EditProfileForm(instance=user)
            return render(request, 'edit_profile.html', {'form': form, 'user':user})

def player_dashboard(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        game_joined  = Game_login.objects.filter(player=user).first()
        if game_joined :
            current_level = game_joined.current_level
            print(current_level)
            level = Level.objects.filter(game=game_joined.games, game_level=current_level).first()
            context = {'game': game_joined, 'user': user, 'level': level}
            return render(request, 'player-dashboard/app.html', context)
        else:
            return redirect('player_home')
    else:
        return HttpResponse("You are not logged in.")
def coordinator_dashboard(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        games = user.games_created.all()
        players = User.objects.filter(game_login__games__in=games)
        print(players)
        total_players = players.count()
        game_player_counts = {}
        for game in games:
            game_player_counts[game.game_name] = game.players.count()
        # context = {'players': players, 'games': games, 'user': user}
        # return render(request, 'coordinator-dashboard/app.html', context)
        # print(games)
        # # Get all players in these games
        # players = []
        # for game in games:
        #     print(game)
        #     players.extend(game.players.all())
        # print(players)
        context = {'players': players, 'games': games, 'user': user, 'total_players': total_players, 'game_player_counts': game_player_counts}
    # except Game.DoesNotExist:
    #     context = {'players': None, 'game': None, 'user': user}
        return render(request, 'coordinator-dashboard/app.html', context)
    else:
        return HttpResponse("You are not logged in.")

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
        print(token)

        # Refresh the user instance to get the updated token value from the database
        # user.refresh_from_db()
        context = {
            'uid': user.uid,
            'email': user.email,
            'name': user.name,
            'token': token,
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
        }
        subject = 'Password reset'
        message = 'Please click on the following link to reset your password: {protocol}://{domain}/password/{uid}/{token}'.format(
            **context)
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        messages.success(request, "Password reset email sent")
        return render(request, 'login.html')

    return render(request, 'login.html')


def password(request, uid=None, token=None):
    if request.method == 'POST':
        email = request.POST['email']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        # Check if the new password and confirm password match
        if new_password != confirm_password:
            return HttpResponse("Passwords don't match")
        # Authenticate the user with the current password
        user = User.objects.filter(email=email).first()
        if user is not None:
            # Hash the new password and update the user object
            user.password = new_password
            user.save()
            # Redirect the user to the login page
            return redirect('login')
        else:
            # Return an error message if authentication fails
            return HttpResponse("Invalid current password")
    else:
        user = None
        if uid is not None and token is not None:
            # Password reset scenario
            user = User.objects.filter(uid=uid).first()
            if user is not None and user.is_password_reset_token_valid(token):
                # Token is valid, allow user to reset password
                return render(request, 'change_password.html', {'uid': uid, 'token': token})
            else:
                # Token is invalid, show error message
                return HttpResponse("Invalid password reset link")
        else:
            # Change password scenario
            if request.user.is_authenticated:
                user = request.user
            else:
                # Redirect to login page if user is not authenticated
                return redirect('login')
        if user is not None:
            return render(request, 'change_password.html', {'user': user})
        else:
            # Return an error message if user is not found
            return HttpResponse("User not found")






def player_home(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        if request.method == 'POST':
            game_id = request.POST['game_id']
            game = Game.objects.filter(game_id=game_id).first()
            if game:
                game_join = Game_login.objects.create(games=game, player=user, current_level=1)
                game_join.save()
                level = Level.objects.filter(game=game_join.games, ).first()
                return redirect(player_dashboard)
                # context = {'game': game_join, 'user': user, 'level': level}
                # return render(request, 'player-dashboard/app.html', context)
            else:
                messages.success(request, "can't find any game with this id.")
                return redirect(player_home)
        else:
            context = {'user': user}
            return render(request, 'player-dashboard/home.html', context)

def check_answer(request,id):
    if 'uid' in request.session:
        uid = request.session['uid']
        user = User.objects.get(uid=uid)
        game_joined = Game_login.objects.get(player=user)
        print(game_joined)
        level_count = Level.objects.filter(game=game_joined.games).count()
        print(level_count)
        level = Level.objects.get(game=game_joined.games, id=id)
        print(level)
        print(level.game_level)
        game_level = level.game_level
        if request.method == 'POST':
            answer = request.POST['answer']
            # Answer = Level.objects.filter(answer=answer)
            if answer == level.answer:
                # request.session['current_level'] = level.id
                # print(level.id)
                # move to the next level
                next_level = game_level + 1
                # print(next_level)
                if next_level <= level_count:
                    game_joined.current_level = next_level
                    game_joined.save()
                    print(game_joined.current_level)
                    # level.game_level = next_level
                    messages.success(request, 'Congratulations! You have moved to the next level.')
                    return redirect('player_dashboard')
                else:
                    messages.success(request, 'Congratulations! You have completed the game.')
                    context = {'game': game_joined, 'user': user}
                    return render(request, 'player-dashboard/app.html',context)
            else:
                messages.error(request, 'Incorrect answer. Please try again.')
                return redirect('check_answer', id)
        else:
            context = {'game_login': game_login, 'level': level, 'user': user}
            return render(request, 'player-dashboard/check_answer.html', context)

def game_login(request):
    id = request.session['uid']
    user = User.objects.get(uid=id)
    if request.method == 'POST':
        id = request.POST['id']
        game_id = request.POST['game_id']
        game = Game.objects.get(game_id=game_id)
        context = {'game': game, 'user': user}
        return render(request, 'player-dashboard/app.html', context)

def player_game_details(request):
    id = request.session['uid']
    user = User.objects.get(uid=id)

    context = {'user': user}
    return render(request, 'player-dashboard/check_answer.html', context)


def player_details(request):
    if 'uid' in request.session:
        id = request.session['uid']

        user = User.objects.get(uid=id)

        # games = Game.objects.filter(creater_id=user.uid)
        games = user.games_created.all()
        print(games)
        game_players = {}
        for game in games:
            print(game)
            # players = Game_login.objects.filter(game=game.game_name)
            # players = User.objects.filter(game_login__games__in=game)
            players = Game_login.objects.filter(games=game)
            print(players)
            game_players[game] = players
            print(game_players)
        context = {'game_players': game_players, 'games': games, 'user': user}
        return render(request, 'coordinator-dashboard/player_details.html', context)
    else:
        messages.error(request, 'You are not logged in')
        return redirect('logout')

def game_create(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        users = User.objects.all()
        if request.method == 'POST':
            game_name = request.POST.get('game_name')
            game_id = request.POST.get('game_id')
            rules = request.POST.get('rules')
            start_date = request.POST.get('start_date')
            game = Game.objects.create(
                    game_name=game_name,
                    game_id=game_id,
                    rules=rules,
                    start_date=start_date,
                    creater_id=user.uid,
                )
            game.save()
            games = user.games_created.all()
            context = {'games': games, 'user': user}
            return render(request, 'coordinator-dashboard/coordinator_game_detail.html', context)
        games = Game.objects.all()
        context = {'user': user, 'games': games}
        return render(request, 'coordinator-dashboard/game_create.html', context)
    else:
        return HttpResponse("You are not logged in.")
def coordinator_game_detail(request):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        # game = Game.objects.get(game_email=email)
        # # games = Game.objects.filter(coordinator=user).all()
        # games = Game.objects.filter(game_email=email)
        # context = {'games': games , 'game': game, 'user': user}
        # return render(request, 'coordinator-dashboard/coordinator_game_detail.html', context)
        try:
            games = Game.objects.filter(creater=user)
            # game = user.games_created.all()
            # games = Level.objects.filter(id=id)
            context = {'games': games, 'user': user}
        except Game.DoesNotExist:
            context = {'game': None, 'user': user}
        return render(request, 'coordinator-dashboard/coordinator_game_detail.html', context)
    else:
        return HttpResponse("You are not logged in.")


def edit_player(request,uid):
    if 'uid' in request.session:
        id = request.session['uid']
        user = User.objects.get(uid=id)
        player = User.objects.get(uid=uid)
        form = EditplayerForm(instance=player)
        if request.method == 'POST':
            form = EditplayerForm(request.POST, instance=player)
            if form.is_valid():
                form.save()
                return redirect('player_details')
        context = {'form': form, 'player': player, 'user': user}
        return render(request, 'coordinator-dashboard/edit_player.html', context)

def delete_player(request,uid,game_id):
    game = Game.objects.get(game_id=game_id)
    player = User.objects.get(uid=uid)
    game_login = Game_login.objects.get(games=game, player=player)
    game_login.delete()

    player.delete()
    return redirect('player_details')


def edit_game(request,id):
    uid = request.session['uid']
    user = User.objects.get(uid=uid)
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
    uid = request.session['uid']
    user = User.objects.get(uid=uid)
    game = Game.objects.get(pk=id)
    print(id)
    if Level.objects.filter(game=game).exists():
        levels = Level.objects.filter(game=game)
        context = {'game': game, 'levels': levels, 'user': user}
        return render(request, 'coordinator-dashboard/view_game.html', context)
    else:
        # return redirect('create_level', id=id)
        context = {'game': game, 'user': user}
        return render(request, 'coordinator-dashboard/view_game.html', context)

def delete_game(request,id):
    game = Game.objects.get(pk=id)
    game.delete()
    return redirect('coordinator_game_detail')

def create_level(request,id):
    if 'uid' in request.session:
        uid = request.session['uid']
        user = User.objects.get(uid=uid)
        game = Game.objects.get(pk=id)
        # form = EditlevelForm(instance=game)
        # if request.method == 'POST':
        #     form = EditlevelForm(request.POST, instance=game)
        #     if form.is_valid():
        #         form.cleaned_data['password_result'] = 'password_result'
        #         form.save()
        #         return redirect('coordinator_game_detail')

        if request.method == 'POST':
            game_level = request.POST['game_level']
            password = request.POST['password']
            answer = request.POST['answer']
            clues = request.POST['clues']
            level = Level.objects.create(
                game=game,
                game_level=game_level,
                password=password,
                answer=answer,
                clues=clues
            )
            level.save()
            # context = {'level': level}
            # return render(request, 'coordinator-dashboard/view_game.html', context)
            return redirect('view_game', id=id)
        else:
            context = {'game': game, 'user': user}
            return render(request, 'coordinator-dashboard/create_level.html', context)

def edit_level(request,id):
    if 'uid' in request.session:
        uid = request.session['uid']
        user = User.objects.get(uid=uid)
        level = Level.objects.get(pk=id)
        print(id)
        if request.method == 'POST':
            level.password = request.POST['password']
            level.answer = request.POST['answer']
            level.clues = request.POST['clues']
            level.save()
            return redirect('view_game', id=level.game.id)
        else:
            context = {'level': level, 'user': user}
            return render(request, 'coordinator-dashboard/edit_level.html', context)

def delete_level(request,id,level_id):
    game = Game.objects.get(pk=id)
    level = Level.objects.get(id=level_id)
    level.delete()
    return redirect('view_game', id=id)