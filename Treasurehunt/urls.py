"""Treasurehunt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('register',views.register),
    path('register_success', views.register_sucess),
    path('login',views.my_login, name='login'),
    path('logout', views.my_logout, name='logout'),
    path('edit_profile', views.edit_profile),
    path('player-dashboard', views.player_dashboard, name='player_dashboard'),
    path('coordinator-dashboard', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('send_test_email',views.send_test_email),
    path('password_reset',views.password_reset),
    path('reset/<str:uid>/<str:token>/', views.password, name='password'),
    path('change_password',views.change_password),
    path('player_game_details',views.player_game_details),
    path('scoreboard',views.scoreboard),
    path('player_details', views.player_details, name='player_details'),
    path('game_create', views.game_create, name='game_create'),
    path('coordinator_game_detail', views.coordinator_game_detail, name='coordinator_game_detail'),
    path('edit_player/<int:uid>', views.edit_player, name='edit_player'),
    path('delete_player/<int:uid>', views.delete_player, name='delete_player'),
    # path('view_player', views.view_player),
    path('analytics', views.analytics, name='analytics'),
    path('edit_game/int:<id>', views.edit_game, name='edit_game'),
    path('view_game/int:<id>', views.view_game, name='view_game'),
    path('delete_game/int:<id>', views.delete_game, name='delete_game'),
    path('edit_level/int:<id>', views.edit_level, name='edit_level')
]
