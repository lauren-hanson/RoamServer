from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Category


class CategoryView(ViewSet):

    def retrieve(self, request, pk):

        category = Category.objects.get(pk=pk)
        serialized = CategorySerializer(category, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):

        category = Category.objects.create(
            type=request.data['type']
        )

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'type',  )