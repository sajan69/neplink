from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import generics, status,viewsets,pagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect

from .forms import ForgotPasswordForm, OTPVerificationForm, CustomUserCreationForm
from .models import OTP, Friendship, User  # Ensure User is imported from your app's models
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, OTPSerializer,
    ForgotPasswordSerializer, OTPVerificationSerializer, PasswordResetSerializer,
    PasswordResetConfirmSerializer, FriendSerializer, FriendshipSerializer,ProfileSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = pagination.PageNumberPagination
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = pagination.PageNumberPagination
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class FriendshipListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = Friendship.objects.filter(from_user=user, accepted=True).values_list('to_user', flat=True)
        return User.objects.filter(id__in=friends)

class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_requests = Friendship.objects.filter(to_user=user, accepted=False).values_list('from_user', flat=True)
        return User.objects.filter(id__in=friend_requests)

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id):
        from_user = request.user
        to_user = get_object_or_404(User, id=to_user_id)
        
        if from_user != to_user:
            friendship, created = Friendship.objects.get_or_create(from_user=from_user, to_user=to_user)
            if not created:
                return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, from_user_id):
        to_user = request.user
        from_user = get_object_or_404(User, id=from_user_id)
        
        friendship = Friendship.objects.filter(from_user=from_user, to_user=to_user, accepted=False).first()
        if friendship:
            friendship.accepted = True
            friendship.save()
            return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, friend_id):
        user = request.user
        friend = get_object_or_404(User, id=friend_id)

        friendship = Friendship.objects.filter(from_user=user, to_user=friend, accepted=True).first() \
                     or Friendship.objects.filter(from_user=friend, to_user=user, accepted=True).first()

        if friendship:
            friendship.delete()
            return Response({'detail': 'Friend removed successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Friendship not found'}, status=status.HTTP_404_NOT_FOUND)


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')

def send_otp_email(user, otp_value):
    subject = 'OTP for Password Reset'
    message = f"Hello {user.username},\n\nYour OTP for password reset is: {otp_value}\n\nThank you!"
    send_mail(subject, message, 'sajanac46@gmail.com', [user.email])

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, 
            username=serializer.validated_data['username'], 
            password=serializer.validated_data['password']
        )
        if user is not None:
            token = RefreshToken.for_user(user)
            return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)
            otp_value = get_random_string(length=6, allowed_chars='1234567890')
            OTP.objects.create(user=user, otp_value=otp_value)
            send_otp_email(user, otp_value)
            return Response({'detail': 'OTP sent to email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp_value = serializer.validated_data['otp_value']
            otp = OTP.objects.filter(user=user, otp_value=otp_value).first()
            if otp:
                otp.delete()  # Delete OTP record after successful verification
                return Response({'detail': 'OTP verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_value = serializer.validated_data['otp_value']
            new_password = serializer.validated_data['new_password']
            
            user = get_object_or_404(User, email=email)
            otp = OTP.objects.filter(user=user, otp_value=otp_value).first()
            if otp:
                user.set_password(new_password)
                user.save()
                otp.delete()  # Delete OTP record after successful verification
                return Response({'detail': 'Password reset successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            otp_value = get_random_string(length=6, allowed_chars='1234567890')
            OTP.objects.create(user=user, otp_value=otp_value)
            send_otp_email(user, otp_value)
            return redirect('users:verify_otp', user_id=user.id)
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_value = form.cleaned_data['otp_value']
            otp = OTP.objects.filter(user=user, otp_value=otp_value).first()
            if otp:
                # OTP validation successful, proceed with password reset
                otp.delete()  # Delete OTP record after successful verification
                return redirect('users:password_reset', user_id=user.id)
            else:
                form.add_error('otp_value', 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'verify_otp.html', {'form': form})

def password_reset(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Update session with new password
            return redirect('users:login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'password_reset.html', {'form': form})



@login_required
def profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    is_friend = False
    friend_request_sent = False
    friend_request_received = False
    friend_request_id = None

    if request.user != profile_user:
        # Check if they are friends
        if Friendship.objects.filter(from_user=request.user, to_user=profile_user, accepted=True).exists() or \
           Friendship.objects.filter(from_user=profile_user, to_user=request.user, accepted=True).exists():
            is_friend = True
        # Check if a friend request is sent
        elif Friendship.objects.filter(from_user=request.user, to_user=profile_user, accepted=False).exists():
            friend_request_sent = True
        # Check if a friend request is received
        elif Friendship.objects.filter(from_user=profile_user, to_user=request.user, accepted=False).exists():
            friend_request_received = True
            friend_request_id = Friendship.objects.get(from_user=profile_user, to_user=request.user, accepted=False).id

    # Get friends
    friendships = Friendship.objects.filter(
        Q(from_user=profile_user, accepted=True) | Q(to_user=profile_user, accepted=True)
    )

    friends = []
    for friendship in friendships:
        if friendship.from_user == profile_user:
            friends.append(friendship.to_user)
        else:
            friends.append(friendship.from_user)

    # Get pending friend requests sent by the profile user
    pending_requests_sent = Friendship.objects.filter(from_user=profile_user, accepted=False)

    # Get incoming friend requests received by the profile user
    incoming_requests = Friendship.objects.filter(to_user=profile_user, accepted=False)

    context = {
        'profile_user': profile_user,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'friend_request_id': friend_request_id,
        'friends': friends,
        'pending_requests_sent': pending_requests_sent,
        'incoming_requests': incoming_requests,
    }
    return render(request, 'profile.html', context)

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.user != to_user:
        friendship, created = Friendship.objects.get_or_create(from_user=request.user, to_user=to_user)
        if not created:
            # If the request already exists, handle accordingly
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required
def accept_friend_request(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id, to_user=request.user)
    friendship.accepted = True
    friendship.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
@login_required
def remove_friend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    friendship = Friendship.objects.filter(from_user=request.user, to_user=user, accepted=True).first()
    if friendship:
        friendship.delete()
    else:
        friendship = Friendship.objects.filter(from_user=user, to_user=request.user, accepted=True).first()
        if friendship:
            friendship.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))