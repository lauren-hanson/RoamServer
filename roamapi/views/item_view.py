from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import Item, Category, Traveler


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

    # def create(self, request):

    #     serializer = ItemSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # item = serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     # {'id': item.id}

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):

        category_id = request.data.get('category')
        category = Category.objects.get(pk=category_id)
        item = Item.objects.create(
            name=request.data['name'],
            category=category,
        )

        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'type', )


class ItemSerializer(serializers.ModelSerializer):\

    class Meta:
        model = Item
        fields = ('id', 'name', 'category',)
