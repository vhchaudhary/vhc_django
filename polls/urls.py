
from django.urls import path
from . import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('user', views.user_data, name='user_data'),
    path('create_person', views.create_person, name='create_person'),
    path('update_person', views.update_person, name='update_person'),
    path('delete_person', views.delete_person, name='delete_person')
]