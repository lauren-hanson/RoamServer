"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import TripTag, Trip, Tag, Traveler


class TripTagView(ViewSet):
    
    def create(self, request):

        try:
            traveler = Traveler.objects.get(user=request.auth.user)
        except Traveler.DoesNotExist:
            return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        try:
            trip = Trip.objects.get(pk=request.data['trip'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid trip Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            tag = Tag.objects.get(pk=request.data['tag'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid tag Id'}, status=status.HTTP_404_NOT_FOUND)

        triptag = TripTag.objects.create(
            trip=trip,
            traveler=traveler,
            tag=tag
        ) 

        serializer = TripTagSerializer(triptag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TripTagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    class Meta:
        model = TripTag
        fields = ('id', 'trip', 'traveler', 'tag')
