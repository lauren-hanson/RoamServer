from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from datetime import datetime
from roamapi.models import Trip, Traveler, Destination, Tag, TripTag, TripDestination


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
            trips = Trip.objects.all()
            # .order_by("start_date")

        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        traveler = Traveler.objects.get(user=request.auth.user)

        trip = Trip.objects.create(
            traveler=traveler,
            start_date=request.data['startDate'],
            end_date=request.data['endDate'],
            notes=request.data['notes'],
            title=request.data['title']
        )

        tags_selected = request.data['tag']

        for tag in tags_selected:
            # trip_tag = TripTag()
            # trip_tag.trip = trip
            # trip_tag.tag = Tag.objects.get(pk=tag)
            # trip_tag.save()
            new_tag = Tag.objects.get(pk=tag)
            trip.tag.add(new_tag)

        # destinations_added = request.data['destination']
        # for destination in destinations_added:
        #     trip_destination = TripDestination()
        #     trip_destination.trip = trip
        #     trip_destination.destination = Destination.objects.get(pk=destination)
        #     trip_destination.save()

        #     new_destination = Destination.objects.get(pk=destination)
        #     trip.destination.add(new_destination)

        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        traveler = Traveler.objects.get(user=request.auth.user)

        trip_to_update = Trip.objects.get(pk=pk)
        trip_to_update.traveler = traveler
        trip_to_update.title = request.data['title']
        trip_to_update.weather = request.data['weather']
        trip_to_update.image_url = request.data['image_url']
        trip_to_update.start_date = request.data['start_date']
        trip_to_update.end_date = request.data['end_date']
        trip_to_update.notes = request.data['notes']
        trip_to_update.public = request.data['public']
        trip_to_update.save()

        tags_selected = request.data['tag']

        current_tag_relationships = TripTag.objects.filter(trip__id=pk)
        current_tag_relationships.delete()

        for tag in tags_selected:
            trip_tag = TripTag()
            trip_tag.trip = trip_to_update
            trip_tag.tag = Tag.objects.get(pk=tag)
            trip_tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        trip.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TripDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state', )

class TravelerSerializer(serializers.ModelSerializer):
    """JSON serializer for reactions
    """
    class Meta:
        model = Traveler
        fields = ('id', 'full_name')

class TripTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'type')


class TripSerializer(serializers.ModelSerializer):

    destination = TripDestinationSerializer(many=True)
    tag = TripTagSerializer(many=True)
    traveler = TravelerSerializer()

    class Meta:
        model = Trip
        fields = ('id', 'start_date', 'end_date', 'notes',
                  'weather', 'destination', 'tag', 'title', 'public', 'image_url','traveler',)
        depth = 1
