
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('get_branches', views.get_branches, name='get_branches'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('send_pass_reset_mail', views.send_pass_reset_mail, name="send_pass_reset_mail"),
    path('pay_fee', views.pay_fee, name='pay_fee'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('pay_done', views.payment_done, name='payment_done'),
]