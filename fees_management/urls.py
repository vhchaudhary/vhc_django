
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('get_branches', views.get_branches, name='get_branches'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('send_pass_reset_mail', views.send_pass_reset_mail, name="send_pass_reset_mail"),
    path('get_amount', views.get_amount, name='get_amount'),
    path('create_payment', views.create_payment, name='create_payment'),
    path('pay_done', views.payment_done, name='payment_done'),


    path('reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html',
                                                        email_template_name='password_reset_email.html',
                                                        subject_template_name='password_reset_subject.txt')),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
            name='password_reset_confirm'),
    re_path(r'^reset/complete/$',
            auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
            name='password_reset_complete'),
]