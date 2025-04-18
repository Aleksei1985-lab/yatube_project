from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path(
      'logout/',
      # Прямо в описании обработчика укажем шаблон, 
      # который должен применяться для отображения возвращаемой страницы.
      # Да, во view-классах так можно! Как их не полюбить.
      LogoutView.as_view(),
      name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # регистрация
    path('signup/', views.SignUp.as_view(), name='signup'),
    # Смена пароля
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), 
         name='password_change_done'),
    
    # Восстановление пароля
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),
] 