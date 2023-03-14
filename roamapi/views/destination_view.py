from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Destination

class DestinationView(ViewSet):

    def retrieve(self, request, pk):

        destination = Destination.objects.get(pk=pk)
        serialized = DestinationSerializer(destination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


    def list(self, request):

        destinations = Destination.objects.all()
        serialized = DestinationSerializer(destinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class DestinationSerializer(serializers.ModelSerializer): 
        class Meta: 
            model = Destination
            fields = ('id', 'location', 'state', 'latitude', 'longitude', )
