from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Trip, Traveler, Destination, Tag


class TripView(ViewSet):

    def retrieve(self, request, pk):

        traveler = Traveler.objects.get(user=request.auth.user)
        try:
            trip = Trip.objects.get(pk=pk)
            if trip.traveler == traveler:
                trip.writer = True
        except Trip.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        trips = []
        traveler = Traveler.objects.get(user=request.auth.user)

        if "user" in request.query_params:
            trips = Trip.objects.filter(traveler_id=traveler)

        else:
            trips = Trip.objects.all().order_by("start_date")

        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        traveler = Traveler.objects.get(user=request.auth.user)

        trip = Trip.objects.create(
            traveler=traveler,
            weather=request.data['weather'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            notes=request.data['notes']
        )

        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        traveler = Traveler.objects.get(user=request.auth.user)

        trip_to_update = Trip.objects.get(pk=pk)
        trip_to_update.traveler = traveler
        trip_to_update.weather = request.data['weather']
        trip_to_update.start_date = request.data['start_date']
        trip_to_update.end_date = request.data['end_date']
        trip_to_update.notes = request.data['notes']
        trip_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        trip.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TripDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state', )


class TripTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'type')


class TripSerializer(serializers.ModelSerializer):

    destination = TripDestinationSerializer(many=True)
    tag = TripTagSerializer(many=True)

    class Meta:
        model = Trip
        fields = ('id', 'start_date', 'end_date', 'notes',
                  'weather', 'destination', 'tag', )
