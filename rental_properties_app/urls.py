from django.urls import path
from . import views


urlpatterns = [
    path('rental', views.RuPropertyListing.as_view(), name="ru-property-listing"),
]