from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Destination, Status


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

# class DestinationStatusSerializer(serializers.ModelSerializer): 

#     class Meta: 
#         model = Status
#         fields = ('status')

class DestinationSerializer(serializers.ModelSerializer):

    # status = DestinationStatusSerializer()

    class Meta:
        model = Destination
        fields = ('id', 'location', 'state',
                  'latitude', 'longitude',  )
