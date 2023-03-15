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
        # traveler = Traveler.objects.get(user=request.auth.user)

        if "status__type" in request.query_params:
            # final_destination = request.query_params('FinalDestination')
            tripdestinations = TripDestination.objects.filter(status__type='Home')
            tripdestinations = TripDestination.objects.filter(status__type='FinalDestination')
            tripdestinations = TripDestination.objects.filter(status__type='Stop')

        else:
            tripdestinations = TripDestination.objects.all()

        serialized = TripDestinationSerializer(tripdestinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class TripSerializer(serializers.ModelSerializer):
    class Meta:

        model = Trip
        fields = ('traveler', 'start_date', 'end_date',
                  'weather', 'notes', 'public',)


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('location', 'state')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('type', )


class TripDestinationSerializer(serializers.ModelSerializer):

    status = StatusSerializer()
    destination = DestinationSerializer()
    trip = TripSerializer()

    class Meta:
        model = TripDestination
        fields = ('trip', 'destination', 'status', )
