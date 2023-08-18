from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('rentals/property/sync', views.sync_properties_from_rental,
         name='sync_properties_from_rental'),
    path('rentals/amenities/sync', views.save_amenities_in_db, name='sync_amenities')]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)