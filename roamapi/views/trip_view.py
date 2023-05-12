from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from datetime import date
from django.db.models import Q
from roamapi.models import Trip, Traveler, Destination, Tag, TripTag, TripDestination, DestinationStatus


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

        elif "subscribed" in request.query_params:
            trips = Trip.objects.filter(traveler__in=Traveler.objects.filter(
                subscribers__user=request.auth.user)).order_by("-publication_date")
            print(trips.query)

        # need to work on this for filtering trips by destinations
        elif "destination" in request.query_params:
            trip_destination = request.query_params['destination']
            trips = Trip.objects.filter(
                trip_by_destination=trip_destination
            )

        # elif "destination" in request.query_params:
        #     trip_status = request.query_params['destination']['status']['type']
        #     trips = Trip.objects.filter(destination_status=trip_status) & (Q(user=request.auth.user))
        #     trip_status = request.query_params['status']['type']
        #     trips = Trip.objects.filter(status__type=trip_status)

        # elif "tag" in request.query_params:
        #     tag_trips = request.query_params.getlist('tag')
        #     trips = Trip.objects.filter(tag_id=tag_trips)

        elif "public" in request.query_params:
            trips = Trip.objects.filter(public=True).order_by('?')

        elif "upcoming" in request.query_params:
            today = date.today()
            # filter trips that have already ended
            trips = Trip.objects.filter(
                Q(end_date__lt=today) & Q(traveler_id=traveler) & Q(complete=False))
            # get trips that have not yet ended
            upcoming_trips = Trip.objects.filter(
                Q(end_date__gte=today) & Q(traveler_id=traveler))
            # merge the two lists
            trips = list(upcoming_trips)

        elif "past" in request.query_params:
            today = date.today()
            # filter trips that have already ended or are ongoing
            past_and_ongoing_trips = Trip.objects.filter(
                Q(end_date__lte=today) & Q(traveler_id=traveler))
            # get trips that have not yet ended
            trips = list(past_and_ongoing_trips) + list(trips)

        else:
            trips = Trip.objects.all()

        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        # try:
        #     traveler = Traveler.objects.get(user=request.auth.user)
        # except Traveler.DoesNotExist:
        #     return Response({'message': 'You sent an invalid token'}, status=status.HTTP_404_NOT_FOUND)

        traveler = Traveler.objects.get(user=request.auth.user)

        trip = Trip.objects.create(
            traveler=traveler,
            start_date=request.data['startDate'],
            end_date=request.data['endDate'],
            notes=request.data['notes'],
            title=request.data['title'],
            image_url=request.data['image_url'],
            public=request.data['public'],
            complete=request.data['complete']
        )

        tags_selected = request.data['tag']

        for tag in tags_selected:
            # trip_tag = TripTag()
            # trip_tag.trip = trip
            # trip_tag.tag = Tag.objects.get(pk=tag)
            # trip_tag.save()
            new_tag = Tag.objects.get(pk=tag)
            trip.tag.add(new_tag)

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
        trip_to_update.complete = request.data['complete']
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


class TripStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DestinationStatus
        fields = ('type', )


class TripDestinationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state',
                  'latitude', 'longitude', 'tips', 'destination_status',)


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
                  'weather', 'destination', 'tag', 'title', 'public', 'complete', 'image_url', 'traveler', 'publication_date', 'writer',)
        depth = 1
