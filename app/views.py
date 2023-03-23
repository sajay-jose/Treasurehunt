from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .models import User,Game
from django.core.mail import send_mail
from django.conf import settings

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
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, game_name=game_name,phonecode=phonecode, phone=phone)
            user.save()
        elif register_as == '2': #player
            game_id = request.POST['game_id']
            user = User.objects.create(name=name, email=email, register_as=register_as, password=password, game_id=game_id, phonecode=phonecode, phone=phone)
            user.save()

        return redirect(register_sucess)

def register_sucess(request):
    return render(request,'register_sucess.html')

def my_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        register_as = request.POST.get('register_as')
        if email and password:
            try:
                user = authenticate(request, username=email, password=password)
                print(user)
                if user is not None:
                    print(register_as, user.register_as)
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

def logout(request):
    if 'email' in request.session:
        request.session.flush()
        return redirect(my_login)

def player_dashboard(request):
    return render(request, 'player-dashboard/app.html')

def coordinator_dashboard(request):
    user = User.objects.all()
    context = {'user': user}
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

def game_details(request):
    return render(request, 'player-dashboard/game_details.html')

def scoreboard(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'player-dashboard/scoreboard.html', context)
def player_details(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'coordinator-dashboard/player_details.html', context)
def game_create(request):
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

    return render(request, 'coordinator-dashboard/game_create.html')

def coordinator_game_detail(request):
    game = Game.objects.all()
    context = {'game': game}
    return render(request, 'coordinator-dashboard/coordinator_game_detail.html', context)
def coordinator_player_dashboard(request):
    return render(request, 'coordinator-dashboard/player_dashboard.html')


def check_id(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        user = authenticate(request, uid=uid)
        if user is not None:
            return render(request, 'coordinator-dashboard/edit_player.html', {'player': user, 'uid': uid} )
        else:
            return HttpResponse("Invalid ID")

def edit_player(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        player = get_object_or_404(User, pk=uid)
        # Handle form submission and save changes to the database
        player.name = request.POST['name']
        player.email = request.POST['email']
        player.phone = request.POST['phone']
        player.save()
        return redirect('player_details')
    else:
        return HttpResponse("error")

    # # Render the edit form with the player's current details pre-filled
    # context = {'player': player}
    # return render(request, 'coordinator-dashboard/edit_player.html', context)

def delete_player(request,uid):
    uid = request.GET.get('uid')
    player = get_object_or_404(User, id=uid)
    if request.method == 'POST':
        player.delete()
        return redirect('player_details')
    else:
        return HttpResponse("Invalid request method")

def view_player(request):
    if request.method == 'GET':
        user = User.objects.filter(uid='uid').all()
        context = {'user': user}
        return render(request, 'coordinator-dashboard/view_player.html', context)

def analytics(request):
    # Get the total number of players registered
    num_players = User.objects.filter(register_as='2').count()

    context = {
        'num_players': num_players
    }

    return render(request, 'coordinator-dashboard/analytics.html', context)