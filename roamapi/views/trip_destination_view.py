from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import TripDestination, Status


class TripDestinationView(ViewSet):

    def retrieve(self, request, pk):

        tripdestination = TripDestination.objects.get(pk=pk)
        serialized = TripDestinationSerializer(tripdestination, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        tripdestinations = TripDestination.objects.all()
        serialized = TripDestinationSerializer(tripdestinations, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class StatusSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Status
        fields = ('isHome', 'isFinalDestination', 'isStop', )

class TripDestinationSerializer(serializers.ModelSerializer):

    status = StatusSerializer()
    
    class Meta:
        model = TripDestination
        fields = ('trip', 'destination', 'status', )
