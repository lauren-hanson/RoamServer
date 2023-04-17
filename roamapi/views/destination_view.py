from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import serializers, status
from roamapi.models import Destination, DestinationStatus


class DestinationView(ViewSet):

    def retrieve(self, request, pk):

        destination = Destination.objects.get(pk=pk)
        serialized = DestinationSerializer(
            destination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        destinations = Destination.objects.all()

        if "destination_status" in request.query_params:
            trip_status = request.query_params['destination_status']
            destinations = Destination.objects.filter(
                destination_status=trip_status)

        elif "not_favorite" in request.query_params:
            favorite = request.query_params['not_favorite']
            destinations = Destination.objects.exclude(
                destination_status=favorite)

        serializer=DestinationSerializer(destinations, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def create(self, request):

        try:
            destination_status_type=DestinationStatus.objects.get(
                pk = request.data['destination_status'])

        except DestinationStatus.DoesNotExist:
            return Response({'message': 'You sent an invalid destinationStatus Id'}, status = status.HTTP_404_NOT_FOUND)

        destination=Destination.objects.create(
            destination_status=destination_status_type,
            location=request.data['location'],
            state=request.data['state'],
            longitude=request.data['longitude'],
            latitude=request.data['latitude'],
            tips=request.data['tips']
        )

        serializer = DestinationSerializer(destination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        destination_status_type = DestinationStatus.objects.get(
            pk=request.data['destination_status'])

        destination_to_update = Destination.objects.get(pk=pk)

        destination_to_update.destination_status = destination_status_type
        destination_to_update.location = request.data['location']
        destination_to_update.state = request.data['state']
        destination_to_update.latitude = request.data['latitude']
        destination_to_update.longitude = request.data['longitude']
        destination_to_update.tips = request.data['tips']

        destination_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):

        destination = Destination.objects.get(pk=pk)
        destination.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class DestinationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DestinationStatus
        fields = ('type', )


class DestinationSerializer(serializers.ModelSerializer):

    destination_status = DestinationStatusSerializer()

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state',
                  'latitude', 'longitude', 'tips', 'destination_status',)
        depth = 1
