from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from roamapi.views import register_user, login_user, TripView, TravelerView, DestinationView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'trips', TripView, 'trip')
router.register(r'travelers', TravelerView, 'traveler')
router.register(r'destinations', DestinationView, 'destination')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
