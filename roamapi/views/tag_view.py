"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Tag

class TagView(ViewSet):
    
    def retrieve(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TagSerializer(tag)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        tags = Tag.objects.order_by('type')

        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        tag = Tag.objects.create(
            type=request.data["type"]
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):

        tag = Tag.objects.get(pk=pk)
        tag.type = request.data["type"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag  
        fields = ('id', 'type') 
