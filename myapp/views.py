from django.shortcuts import render
from rest_framework import status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User, Audio
from .serializers import UserSerializer, AudioSerializer
import bcrypt
import requests
import os
import speech_recognition as sr
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_signup_email
from django.http import HttpResponse
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from config import FIXED_TOKEN

@api_view(['POST'])
def signup(request):
    # Create a mutable copy of the request data
    data = request.data.copy()

    # Hash the password
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        send_signup_email(data['email'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(email, password)
    try:
        user = User.objects.get(email=email)
        print(user)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user_serializer = UserSerializer(user)
            # Use fixed token
            response_data = {
                'token': FIXED_TOKEN,
                'user': user_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def convert(request):
    print(request.data)
    tts = request.data.get('tts')
    print(tts)
    
    if tts == 'true':
        params = {
            'speaker': request.data['model_id'],
            'tts': request.data['tts'],
            'text': request.data['text'],
            'language-id': 'en',
        }

        # Check if 'reference_wav' is provided
        reference_wav = request.FILES.get('reference_wav')
        if reference_wav:
            # Save the audio file and get the file path
            file_path = reference_wav.name
            # Save the file to the media directory
            fs = FileSystemStorage(location='media/')
            filename = fs.save(file_path, reference_wav)
            file_url = fs.url(filename)
            params['style_wav'] = reference_wav.read()

        if not params['text'] and not params.get('style_wav'):
            return Response({'detail': f"Missing parameters: text or reference_wav is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Make the POST request to the TTS API
        response = requests.post('http://82.112.237.222:5002/api/tts', headers=params, data=params)
        audio_content = response.content
        response = HttpResponse(audio_content, content_type='audio/wav')
        response['Content-Disposition'] = 'attachment; filename="output.wav"'

        # Save the entry in the Audio database
        user = User.objects.get(id=request.data['userid'])
        Audio.objects.create(
            name=user.full_name,
            location=file_path if reference_wav else None,
            text=params['text'],
            user=user,
            datetime=timezone.now()
        )

        return response

    else:
        audio_file = request.FILES.get('reference_wav')
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Save the text entry in the Audio database
        user = User.objects.get(id=request.data['userid'])
        Audio.objects.create(
            name=user.full_name,
            text=text,
            user=user,
            datetime=timezone.now()
        )

        return Response({'text': text}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def profile(request):
    # Validate the token
    print(request)
    auth_token = request.headers.get('Authorization')
    userid = request.GET.get('id')
    print(userid)
    if not auth_token or auth_token != f"Token {FIXED_TOKEN}":
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=userid)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def all_profiles(request):
    # Validate the token
    print("user request")
    print('User:', request.query_params)
    print('Token:', request.headers.get('Authorization'))
    
    auth_token = request.headers.get('Authorization')
    if not auth_token or auth_token != f"Token {FIXED_TOKEN}":
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    if not request.query_params.get('is_admin'):
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_audio(request):
    # Validate the token
    print("Audio Request")
    print('User:', request.query_params)
    print('Token:', request.headers.get('Authorization'))
    auth_token = request.headers.get('Authorization')
    if not auth_token or auth_token != f"Token {FIXED_TOKEN}":
        print("Token has been rejected.")
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    # Check if the user has admin privileges
    if not request.query_params.get('is_admin'):
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    audios = Audio.objects.all()
    serializer = AudioSerializer(audios, many=True)
    print("Gotten all audios")
    print(audios)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    try:
        user = User.objects.get(email=email)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def delete_user(request, user_id):
    print("receive request to delete user")
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def confirm_user(request):
    user_id = request.data.get('userId')
    
    try:
        user = User.objects.get(id=user_id)
        user.verified = True  # Assuming you have a 'Profile' model with 'verified' field
        user.save()
        return Response({"message": "User confirmed successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)    
