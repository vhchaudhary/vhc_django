
from django.urls import path
from . import views


urlpatterns = [
    path('oxford', views.oxford, name='oxford'),
    ]