
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.log_in, name='login'),
    path('get_branches', views.get_branches, name='get_branches'),
    path('register', views.register, name='register'),
]