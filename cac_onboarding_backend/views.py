from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

from django.contrib.auth import login, logout
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import json



from .serializers import *

# @api_view(['GET','POST'])
# def UserView(request):

#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#     if request.method == 'GET':
#         user = User.objects.all()
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data)
    
@api_view(['POST'])
def register_api(request):

    seralizer = RegisterSeralizer(data=request.data)
    
    if seralizer.is_valid():
        seralizer.save()
        return Response({'message':'Register Sucessfully'}, status=status.HTTP_201_CREATED)
    
    return Response({'message':'seralizer has errors'}, status=status.HTTP_406_NOT_ACCEPTABLE)



@api_view(['POST'])
def login_api(request):
    seralizer = LoginSeralizer(data=request.data)      

    
          
    session = SessionStore()
    if seralizer.is_valid():
        user = seralizer.validate(request.data)


        if user is not None:
            login(request,user)
            
            
            session['user_id'] = user.id
            session['user_username'] = user.username
            session.create()
       

            return Response({'Message':'Login successful','session_key':session.session_key},status=status.HTTP_200_OK)  
        else:
            return Response({'Message':"User is None"},status=status.HTTP_404_NOT_FOUND) 
    else:
        return Response({'Message':'It is not valid'},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def user_profile(request):
    session_key = request.data.get('session_key')

    try:
        session = Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        return Response({'Message': 'Invalid session key'}, status=status.HTTP_404_NOT_FOUND)

    session_data = session.get_decoded()
    username = session_data.get('username')

    return Response({'username': username})


def process_logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logout(request)
        session_key = data.get('session_key')

        session = Session.objects.get(session_key=session_key)
        session.expire_date = timezone.now()
        session.save()

        now = timezone.now()
        expired_sessions = Session.objects.filter(expire_date__lt=now)

        

    # Deleting the expired sessions
        expired_sessions.delete()

        reponse = redirect('home_view')
  
        reponse.set_cookie('session_key',session_key, max_age=1)

        return reponse