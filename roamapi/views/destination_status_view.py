from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roamapi.models import DestinationStatus


class DestinationStatusView(ViewSet):

    def retrieve(self, request, pk):
        try:
            destination_status = DestinationStatus.objects.get(pk=pk)

        except DestinationStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DestinationStatusSerializer(destination_status)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        destination_status = DestinationStatus.objects.order_by('type')

        serializer = DestinationStatusSerializer(destination_status, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def create(self, request):

    #     status_type = DestinationStatus.objects.create(
    #         type=request.data["type"]
    #     )
    #     serializer = DestinationStatusSerializer(status)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk):

    #     status_type = DestinationStatus.objects.get(pk=pk)
    #     status_type.type = request.data["type"]
    #     status_type.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk):
    #     status_type = DestinationStatus.objects.get(pk=pk)
    #     status_type.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


class DestinationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationStatus
        fields = ('id', 'type', )
