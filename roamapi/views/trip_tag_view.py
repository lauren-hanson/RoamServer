"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import TripTag, Trip, Tag, Traveler


class TripTagView(ViewSet):

    def create(self, request):
        
        try:
            trip = Trip.objects.get(pk=request.data[0]['trip_id'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid trip Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            tag = Tag.objects.get(pk=request.data[0]['tag_id'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid tag Id'}, status=status.HTTP_404_NOT_FOUND)

        triptag = TripTag.objects.create(
            trip=trip,
            tag=tag
        )

        serializer = TripTagSerializer(triptag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TripTagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""

    class Meta:
        model = TripTag
        fields = ('id', 'trip', 'tag',)
