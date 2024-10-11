from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='profile_view'),
    path('change-password/', views.change_password, name='change_password'),
]
