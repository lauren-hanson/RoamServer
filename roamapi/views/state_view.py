from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import State

class StateView(ViewSet): 

    def retrieve(self, request, pk): 

        try:
            state = State.objects.get(pk=pk)

        except State.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # passes the instance stored in state through serializer to become a JSON stringified object and assigns it to serializer variable
        serializer = StateSerializer(state)

        # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request): 
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StateSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = State 
        fields = ('id', 'label', )