"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Tag


class TagView(ViewSet):
    """Roam tags view"""

    def retrieve(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)

        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # passes the instance stored in tag through serializer to become a JSON stringified object and assigns it to serializer variable
        serializer = TagSerializer(tag)

        # returns serializer data to the client as a response. Response body is JSON stringified object of requested data.
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all tags
        Returns:
            Response -- JSON serialized list of tags
        """
        # Make connection with server to retrieve a query set of all tags items requested by client and assign the found instances to the tags variable
        # tags = Tag.objects.all()
        tags = Tag.objects.order_by('type')
        # passes instances stored in tags variable to the serializer class to construct data into JSON stringified objects, which it then assigns to variable serializer
        serializer = TagSerializer(tags, many=True)

        # Constructs response and returns data requested by the client in the response body as an array of JSON stringified objects
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations
        Returns
            Response -- JSON serialized tag instance
        """

        tag = Tag.objects.create(
            type=request.data["type"]
        )
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)
        tag.type = request.data["type"]
        tag.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types"""
    # Converts meta data requested to JSON stringified object using Tag as model
    class Meta:  # configuration for serializer
        model = Tag  # model to use
        fields = ('id', 'type')  # fields to include
