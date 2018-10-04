
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('get_branches', views.get_branches, name='get_branches'),
]