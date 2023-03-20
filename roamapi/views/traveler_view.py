from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from rest_framework.decorators import action
from django.contrib.auth.models import User
from roamapi.models import Traveler, Subscription


class TravelerView(ViewSet):

    # def retrieve(self, request, pk):

    #     traveler = Traveler.objects.get(pk=pk)
    #     serialized = TravelerSerializer(traveler, context={'request': request})
    #     return Response(serialized.data, status=status.HTTP_200_OK)

    # def list(self, request):

    #     travelers = Traveler.objects.all()
    #     serialized = TravelerSerializer(travelers, many=True)
    #     return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        """Handle GET requests for single author

        Returns:
            Response -- JSON serialized author
        """
        user = Traveler.objects.get(user=request.auth.user)
        subscriptions = Subscription.objects.all()
        subscriptions = subscriptions.filter(subscriber_id=user)

        try:
            traveler = Traveler.objects.get(pk=pk)
            subscriptions = subscriptions.filter(traveler_id=traveler)
            if subscriptions:
                traveler.subscribed = True
            else:
                traveler.subscribed = False

        except Traveler.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        serialized = TravelerSerializer(traveler, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """Handle GET requests to get all travelers

        Returns:
            Response -- JSON serialized list of travelers
        """
        travelers = Traveler.objects.all()
        # travelers = Traveler.objects.annotate(
        #     followers_count=Count('subscribers')
        # )

        for traveler in travelers:
            subscriptions = Subscription.objects.filter(Q(subscriber__user=request.auth.user) & Q(traveler_id=traveler))
            if subscriptions:
                traveler.subscribed = True
            else:
                traveler.subscribed = False

        serializer = TravelerSerializer(travelers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(methods=['post'], detail=True)
    def subscribe(self, request, pk):
        """Post request for a user to sign up for an event"""

        current_user = Traveler.objects.get(user=request.auth.user)
        traveler = Traveler.objects.get(pk=request.data)
        traveler.subscribers.add(current_user)
        return Response({'message': 'Subscriber added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def unsubscribe(self, request, pk):
        """Delete request for a user to leave an event"""

        current_user = Traveler.objects.get(user=request.auth.user)
        author = Traveler.objects.get(pk=pk)
        author.subscribers.remove(current_user)
        return Response({'message': 'Subscriber removed'}, status=status.HTTP_204_NO_CONTENT)


class SubscriberSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Traveler
        fields = ('id', 'full_name')


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'date_joined')


class TravelerSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)
    subscriber = SubscriberSerializer(many=True)

    class Meta:
        model = Traveler
        fields = ('id', 'user', 'bio', 'profile_image_url', 'subscriber', 'subscribed',)
