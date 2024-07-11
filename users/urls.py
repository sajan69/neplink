from django.urls import path
from .views import AcceptFriendRequestView, FriendRequestListView, RemoveFriendView, SendFriendRequestView, login_view, register_user, logout_view, RegisterView, LoginView, ForgotPasswordView, VerifyOTPView, PasswordResetView, PasswordResetConfirmView,FriendshipListView
from . import views

app_name = 'users'


urlpatterns = [
    #Web views
    path('login/', login_view, name='login'),
    path('register/', register_user, name='register'), 
    path('logout/', logout_view, name='logout'),
      path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('password-reset/<int:user_id>/', views.password_reset, name='password_reset'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('send-friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:friendship_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('remove-friend/<int:user_id>/', views.remove_friend, name='remove_friend'),

    # API views
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='api_forgot_password'),
    path('api/verify-otp/<int:user_id>/', VerifyOTPView.as_view(), name='api_verify_otp'),
    path('api/password-reset/<int:user_id>/', PasswordResetView.as_view(), name='api_password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    path('api/friends/', FriendshipListView.as_view(), name='friend_list'),
    path('api/friend-requests/', FriendRequestListView.as_view(), name='friend_request_list'),
    path('api/send-friend-request/<int:to_user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('api/accept-friend-request/<int:from_user_id>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('api/remove-friend/<int:friend_id>/', RemoveFriendView.as_view(), name='remove_friend'),
]
