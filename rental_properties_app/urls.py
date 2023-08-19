from django.urls import path
from . import views

urlpatterns = [
    path('rentals/property/sync', views.sync_properties_from_rental,
         name='sync_properties_from_rental'),
    path('rentals/amenities/sync', views.save_amenities_in_db, name='sync_amenities'),
    path('rentals/properties/listing', views.listing_of_properties, name='properties_list')]
