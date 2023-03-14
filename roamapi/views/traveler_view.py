from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Traveler

class TravelerView(ViewSet):

    def retrieve(self, request, pk):

        traveler = Traveler.objects.get(pk=pk)
        serialized = TravelerSerializer(traveler, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


    def list(self, request):

        travelers = Traveler.objects.all()
        serialized = TravelerSerializer(travelers, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class TravelerSerializer(serializers.ModelSerializer): 
        class Meta: 
            model = Traveler
            fields = ('id', 'user', 'bio', 'profile_image_url', )
