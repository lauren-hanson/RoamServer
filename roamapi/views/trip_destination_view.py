from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import serializers, status
from roamapi.models import TripDestination, Status, Destination, Trip, Traveler


class TripDestinationView(ViewSet):

    def retrieve(self, request, pk):

        tripdestination = TripDestination.objects.get(pk=pk)
        serialized = TripDestinationSerializer(
            tripdestination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        tripdestinations = TripDestination.objects.all()

        traveler = Traveler.objects.get(user=request.auth.user)
        tripdestinations = tripdestinations.filter(trip__traveler=traveler)

        if "status" in request.query_params:
            trip_status = request.query_params['status']
            tripdestinations = tripdestinations.filter(status_id=trip_status)

        elif "trip" in request.query_params:
            destByTrip = request.query_params['trip']
            tripdestinations = TripDestination.objects.filter(trip=destByTrip)

        serialized = TripDestinationSerializer(tripdestinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            trip = Trip.objects.get(pk=request.data['trip'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid trip Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            destination = Destination.objects.get(
                pk=request.data['destination'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid destination Id'}, status=status.HTTP_404_NOT_FOUND)

        try:
            destination_status = Status.objects.get(
                pk=request.data['status'])
        except Trip.DoesNotExist:
            return Response({'message': 'You sent an invalid status Id'}, status=status.HTTP_404_NOT_FOUND)

        tripdestination = TripDestination.objects.create(
            trip=trip,
            destination=destination,
            status=destination_status
        )

        serializer = TripDestinationSerializer(tripdestination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        tripdestination = TripDestination.objects.get(pk=pk) 
        tripdestination.status_id = 4
        tripdestination.save()

        serialized = TripDestinationSerializer( 
            tripdestination, context={'request' : request}
        )
        return Response(serialized.data, status=status.HTTP_200_OK)



class TravelerSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Traveler
        fields = ('id', 'full_name')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('type', )


class TripSerializer(serializers.ModelSerializer):
    class Meta:

        traveler = TravelerSerializer()

        model = Trip
        fields = ('id', 'traveler', 'start_date', 'end_date',
                  'weather', 'notes', 'public',)


class DestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('location', 'state', 'latitude', 'longitude', 'tips',)


class TripDestinationSerializer(serializers.ModelSerializer):

    destination = DestinationSerializer()
    trip = TripSerializer()
    status = StatusSerializer()

    class Meta:
        model = TripDestination
        fields = ('trip', 'destination', 'status',)
