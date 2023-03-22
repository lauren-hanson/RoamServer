from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Destination


class DestinationView(ViewSet):

    def retrieve(self, request, pk):

        destination = Destination.objects.get(pk=pk)
        serialized = DestinationSerializer(
            destination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        destinations = Destination.objects.all()
        serialized = DestinationSerializer(destinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        destination = Destination.objects.create(
            location=request.data['location'],
            state=request.data['state'],
            longitude=request.data['longitude'], 
            latitude=request.data['latitude']
        )

        serializer = DestinationSerializer(destination)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        destination_to_update = Destination.objects.get(pk=pk)

        destination_to_update.location = request.data['location']
        destination_to_update.state = request.data['state']
        # destination_to_update.latitude = request.data['latitude']
        # destination_to_update.longitude = request.data['longitude']

        destination_to_update.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):

        destination = Destination.objects.get(pk=pk)
        destination.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    
class DestinationSerializer(serializers.ModelSerializer):

    # status = DestinationStatusSerializer()

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state', 'latitude', 'longitude', )
