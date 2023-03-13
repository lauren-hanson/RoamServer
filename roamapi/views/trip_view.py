from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Trip

class TripView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):

        trip = Trip.objects.get(pk=pk)
        serialized = TripSerializer(trip, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


    def list(self, request):

        trips = Trip.objects.all()
        serialized = TripSerializer(trips, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class TripSerializer(serializers.ModelSerializer): 
        class Meta: 
            model = Trip
            fields = ('id', 'start_date', 'end_date', 'notes', )
