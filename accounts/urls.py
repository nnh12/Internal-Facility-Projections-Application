from django.urls import path

from . import views

urlpatterns = [
    path('updateLogin', views.updateLogin, name='updateLogin'),
]