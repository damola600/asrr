from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from google_auth_oauthlib.flow import Flow
from .models import GoogleCalendarConnection
from google.oauth2.credentials import Credentials
import os
from dotenv import load_dotenv
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from pathlib import Path
from user_events.services import refresh_user_calendar

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI =  os.getenv("REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")
# Create your views here.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]

@login_required
def google_connect(request):
    print("REDIRECT_URI =", REDIRECT_URI)
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        autogenerate_code_verifier=True
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    request.session["google_oauth_state"] = state
    request.session["google_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)

@login_required
def google_callback(request):
    
    print("\n=== GOOGLE CALLBACK STARTED ===")
    print("User:", request.user.email)
    
    state = request.session.get(
        "google_oauth_state"
    )

    code_verifier = request.session.get(
        "google_code_verifier"
    )

    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = (
        REDIRECT_URI
    )

    if code_verifier:
        flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=
            request.build_absolute_uri()
    )

    credentials = flow.credentials

    connection, created = (
        GoogleCalendarConnection.objects
        .get_or_create(
            user=request.user
        )
    )

    connection.access_token = (
        credentials.token
    )

    if credentials.refresh_token:
        connection.refresh_token = (
            credentials.refresh_token
        )

    connection.token_uri = (
        credentials.token_uri
    )

    connection.scopes = " ".join(
        credentials.scopes or []
    )

    connection.token_expiry = (
        credentials.expiry
    )

    connection.connected = True

    connection.save()
    
    print("Google connection saved")
    print("Connected:", connection.connected)


    # ---------------------------------
    # GOOGLE CONNECTION COMPLETES SETUP
    # ---------------------------------

    member = request.user.profile

    if not member.setup_complete:
        member.setup_complete = True

        member.save(
            update_fields=[
                "setup_complete"
            ]
        )
    
    print("Starting calendar refresh...")
       
    refresh_user_calendar(request.user)
    
    print("Calendar refresh finished")
    print("=== GOOGLE CALLBACK FINISHED ===\n")
    
    
    return redirect(
        f"{FRONTEND_URI}/setup?google"
    )

def get_user_google_credentials(user):
    if not hasattr(user, "google_calendar_connection"):
        raise ValueError("User has not connected Google Calendar.")
        
    connection = user.google_calendar_connection
    
    if not connection.connected:
        raise ValueError("Google Calendar connection is not active.")

    credentials = Credentials(
        token=connection.access_token,
        refresh_token=connection.refresh_token,
        token_uri=connection.token_uri,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=connection.scopes.split()
    )

    return credentials


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def google_calendar_status(request):
    connected = (
        hasattr(request.user, "google_calendar_connection")
        and request.user.google_calendar_connection.connected
    )

    return Response({
        "connected": connected
    })