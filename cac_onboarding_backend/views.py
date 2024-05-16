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

from django.core.exceptions import ObjectDoesNotExist
import logging


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

@api_view(['POST'])
def process_logout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logout(request)
        session_key = data.get('session_key')

    try:
        session = Session.objects.get(session_key=session_key)
        session.expire_date = timezone.now()
        session.save()

        now = timezone.now()
        expired_sessions = Session.objects.filter(expire_date__lt=now)

        


        expired_sessions.delete()
        return Response({'Message':'session deleted'})
    except ObjectDoesNotExist:
            logging.error("Session with key {} does not exist.".format(session_key))
            return Response({'Error':'Session not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
            logging.error("Error while processing logout: {}".format(str(e)))
            return Response({'Error':'An error occurred while processing logout.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from django.http import JsonResponse
from .models import Location


# The location list takes all the data in the "LOCATION MODEL"
# Transformes into json format and return it to the web
def location_list(request):
    locations = Location.objects.all()
    data = [{'streetname': location.streetname, 'durationtime': location.durationtime, 'importance': location.importance} for location in locations]
    return JsonResponse(data, safe=False)


@api_view(['POST'])
def create_location(request):
     if request.method == 'POST':
          serializer = LocationSerializer(data=request.data)
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     


from .serializers import LocationSerializer
from .utils import calculate_cost

@api_view(['POST'])
def add_location(request):
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.save()
            # Transform duration to cost
            location.cost = calculate_cost(location.duration)
            location.save()
            # Return the updated serializer data with the cost included
            return Response(LocationSerializer(location).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .utils import haversine, dijkstra

@api_view(['GET'])
def best_route(request, start_id, end_id):
    try:
        start_location = Location.objects.get(id=start_id)
        end_location = Location.objects.get(id=end_id)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)

    locations = Location.objects.all()
    graph = build_graph(locations)

    path = dijkstra(graph, start_location.id, end_location.id)

    if path is None:
        return Response({'error': 'No path found between the locations.'}, status=status.HTTP_404_NOT_FOUND)

    route = [Location.objects.get(id=location_id).name for location_id in path]

    return Response({'route': route}, status=status.HTTP_200_OK)

def build_graph(locations):
    graph = {}
    for location in locations:
        graph[location.id] = {}
        for other_location in locations:
            if location.id != other_location.id:
                distance = haversine(location.latitude, location.longitude, other_location.latitude, other_location.longitude)
                graph[location.id][other_location.id] = distance
    return graph












from .shortestpath import dijkstra, haversine
@api_view(['GET'])
def get_shortest_path(request):
    if request.method =='GET':
              graph = {
        "A": {"B": 10, "C": 15},
        "B": {"A": 10, "C": 5},
        "C": {"A": 15, "B": 5}
    }

    # Example coordinates for points
    coordinates = {
        "A": (40.7128, -74.0060),  # New York
        "B": (34.0522, -118.2437), # Los Angeles
        "C": (41.8781, -87.6298)   # Chicago
    }

    start = "A"
    end = "C"

    shortest_path = dijkstra(graph, start, end)
    if shortest_path:
        print("Shortest path:", shortest_path)
        total_distance = 0
        for i in range(len(shortest_path) - 1):
            node1 = shortest_path[i]
            node2 = shortest_path[i + 1]
            lat1, lon1 = coordinates[node1]
            lat2, lon2 = coordinates[node2]
            distance = haversine(lat1, lon1, lat2, lon2)
            total_distance += distance
        print("Total distance:", total_distance, "km")
    else:
        print("No path found")

