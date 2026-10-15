from .serializers import RegistrationSerializer, MemberSerializer, SunnahPreferenceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from datetime import datetime, date
from prayers.services import save_prayer_data
from .services import build_user_schedule
from user_events.prayer_services import build_user_prayer_events
from user_events.services import refresh_user_calendar
from django.views.decorators.csrf import ensure_csrf_cookie
from .tasks import send_welcome_email
from user_events.tasks import sync_user_calendar_task

@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_cookie(request):
    return Response(
        {
            "message": "CSRF cookie set."
        },
        status=status.HTTP_200_OK
    )
# Create your views here.

now = datetime.now()
curr_year = now.year
curr_mnth = now.month

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        with transaction.atomic():
            user = serializer.save()
            login(request._request, user)
            
        send_welcome_email.delay(user.email)
        
        return Response(
            {
                "message": "User created successfully.",
                "user": {
                    "email": user.email
                },
                "setup_complete": False,
                "google_calendar_connected": False
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(username=email, password=password)
    
    if user is None:
        return Response(
            {
                "error": "Invalid email or password."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    login(request._request, user)
    
    member = user.profile
    google_connected = False
    
    connection = getattr(user, "google_calendar_connection", None)
    
    if connection:
        google_connected = (connection.connected)
    
    return Response(
        {
            "message": "Login successful.",
            "username": user.email,
            "setup_complete": member.setup_complete,
            "google_calendar_connected": google_connected,
        }, status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(
        request._request
    )

    return Response(
        {
            "message": "Logged out successfully."
        }, status=status.HTTP_200_OK
    )
    
@api_view(['GET', 'PATCH'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    member = request.user.profile
    
    if request.method == 'GET':
        serializer = MemberSerializer(member)
        
        connection = getattr(request.user, "google_calendar_connection", None)
        
        google_connected = (connection is not None and connection.connected)
        
        data = serializer.data
        
        data["google_calendar_connected"] = google_connected
        
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == 'PATCH':
        serializer = MemberSerializer(member, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            member = serializer.save()
            
            if getattr(serializer, "member_update", False):
                user_id = request.user.id
                
                transaction.on_commit(lambda user_id=user_id: sync_user_calendar_task.delay(user_id))
            
            return Response(
                {
                    'message': 'User profile successfully updated',
                    'profile': serializer.data,
                    'calendar_sync_queued': bool(getattr(serializer, 'member_update', False)),
                }, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PATCH'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def sunnah_pref(request):
    sunnah = request.user.sunnah_pref
    
    if request.method == 'GET':
        serializer = SunnahPreferenceSerializer(sunnah)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    if request.method == 'PATCH':
        serializer = SunnahPreferenceSerializer(sunnah, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            serializer.save()
            
            if getattr(serializer, 'sunnah_update', False):
                user_id = request.user.id
                
                transaction.on_commit(lambda user_id=user_id: sync_user_calendar_task.delay(user_id))
                refresh_user_calendar(request.user)
            
            return Response(
                {
                    'message': 'Sunnah preferences updated successfully',
                    'preferences': serializer.data,
                    'calendar_sync_queued': bool(getattr(serializer, 'sunnah_update', False))
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
                
