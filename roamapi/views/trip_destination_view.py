from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import TripDestination, Status, Destination, Trip, Traveler


class TripDestinationView(ViewSet):

    def retrieve(self, request, pk):

        tripdestination = TripDestination.objects.get(pk=pk)
        serialized = TripDestinationSerializer(
            tripdestination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        # tripdestinations = TripDestination.objects.all()
        # serialized = TripDestinationSerializer(tripdestinations, many=True)
        # return Response(serialized.data, status=status.HTTP_200_OK)

        tripdestinations = []

        if "status__type" in request.query_params:
            tripdestinations = TripDestination.objects.filter(
                status__type='Home')
            
        elif "trip" in request.query_params:
            destination_trip = request.query_params['trip']
            tripdestinations = TripDestination.objects.filter(
                trip_id=destination_trip)

        else:
            tripdestinations = TripDestination.objects.all()

        serialized = TripDestinationSerializer(tripdestinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        try:
            trip = Trip.objects.get(pk=request.data[0]['trip_id'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid trip Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            destination = Destination.objects.get(
                pk=request.data[0]['destination'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid destination Id'}, status=status.HTTP_404_NOT_FOUND)

        tripdestination = TripDestination.objects.create(
            trip=trip,
            destination=destination
        )

        serializer = TripDestinationSerializer(tripdestination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TripSerializer(serializers.ModelSerializer):
    class Meta:

        model = Trip
        fields = ('id', 'traveler', 'start_date', 'end_date',
                  'weather', 'notes', 'public',)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('location', 'state', 'latitude', 'longitude', )

class TripDestinationSerializer(serializers.ModelSerializer):

    destination = DestinationSerializer()
    trip = TripSerializer()

    class Meta:
        model = TripDestination
        fields = ('trip', 'destination',  )
