from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Item, Category


class ItemView(ViewSet):

    def retrieve(self, request, pk):

        item = Item.objects.get(pk=pk)
        serialized = ItemSerializer(item, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):

        items = Item.objects.all()

        items_by_category = {}

        for item in items: 
            category = item.category.type
            if category not in items_by_category: 
                items_by_category[category] = []
            items_by_category[category].append(ItemSerializer(item).data) 

        return Response(items_by_category, status=status.HTTP_200_OK)
    

class ItemCategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = ('id', 'type', )

class ItemSerializer(serializers.ModelSerializer):\

    class Meta:
        model = Item
        fields = ('id', 'name', 'category',  )
