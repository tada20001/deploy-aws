from django.contrib.auth import views as auth_views
from django.urls import path, include
from .forms import MyAuthenticationForm
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signup/artist/', views.ArtistSignupView.as_view(), name='artist_signup'),
    path('signup/client/', views.ClientSignupView.as_view(), name='client_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=MyAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('login/url/', views.RequestLoginViaUrlView.as_view(), name='request_login_via_url'),
    path('login/<uidb64>/<token>/', views.login_via_url, name='login_via_url'),

    path('password_change/', views.MyPasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', views.MyPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/<uidb64>/<token>/', views.MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/artist_edit/', views.profile_edit_artist, name='profile_edit_artist'),
    path('profile/client_edit/', views.profile_edit_client, name='profile_edit_client'),

]
