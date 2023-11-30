from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('', views.home, name="home"),
    path('liga/<int:liga_id>/', views.liga_detail, name="liga_detail"),
    path('liga/crear_partido/', views.crear_partido, name="crear_partido"),
]
