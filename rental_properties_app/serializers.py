from rental_properties_app.models import Amenities, Propertyavailabilityprices, Propertybasicinfo, Propertycharges, Propertycheckincheckout, Propertydescription, Propertyimages
from rest_framework import serializers


class PropertyBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propertybasicinfo
        fields = '__all__'

class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'

class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propertyimages
        fields = '__all__'

class PropertyChargesSerializer(serializers.ModelSerializer):
    is_optional = serializers.BooleanField(default=0)
    class Meta:
        model = Propertycharges
        fields = '__all__'

class PropertyAvailabilityPricesSerializer(serializers.ModelSerializer):
    is_price = serializers.BooleanField(default=False)
    class Meta:
        model = Propertyavailabilityprices
        fields = '__all__'


class PropertyCheckincheckoutSerializer(serializers.ModelSerializer):
    prior_days = serializers.IntegerField(default=0)
    checkin_time_from = serializers.CharField(default="00:00", max_length=50)
    checkin_time_to = serializers.CharField(default="00:00", max_length=50)
    checkout_time = serializers.CharField(default="00:00", max_length=50)
    checkinplace = serializers.CharField(default="at_the_apartment", max_length=50)
    late_arrival_fee_from = serializers.CharField(default="00:00", max_length=50)
    late_arrival_fee_to = serializers.CharField(default="00:00", max_length=50)
    late_arrival_fee_cost = serializers.FloatField(default=0)
    early_departure_fee_from = serializers.CharField(default="00:00", max_length=50)
    early_departure_fee_to = serializers.CharField(default="00:00", max_length=50)
    early_departure_fee_cost = serializers.FloatField(default=0)
    class Meta:
        model = Propertycheckincheckout
        fields = '__all__'

class PropertyAllInfoSerializer(serializers.ModelSerializer):
    available_prices = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    charges = serializers.SerializerMethodField()
    checkin_checkout = serializers.SerializerMethodField()

    def query_amenities_data(self, obj):
        listing_obj = Amenities.objects.filter(property_id=obj.property_id)
        return AmenitiesSerializer(listing_obj, many=True).data

    def get_available_prices(self, obj):
        obj = Propertyavailabilityprices.objects.filter(propertyinfo=obj.id)
        return PropertyAvailabilityPricesSerializer(obj, many=True).data
    def get_amenities(self, obj):
        secondary_data = self.query_amenities_data(obj)
        return secondary_data
    def get_images(self, obj):
        obj = Propertyimages.objects.filter(propertyinfo=obj.id)
        return PropertyImagesSerializer(obj, many=True).data
    def get_charges(self, obj):
        obj = Propertycharges.objects.filter(propertyinfo=obj.id)
        return PropertyChargesSerializer(obj, many=True).data
    def get_checkin_checkout(self, obj):
        obj = Propertycheckincheckout.objects.filter(propertyinfo=obj.id)
        return PropertyCheckincheckoutSerializer(obj, many=True).data

    class Meta:
        model = Propertybasicinfo
        fields = ('id', 'property_id', 'group', 'property_name', 'property_type', 'can_sleep_max',
                  'floor', 'size', 'street', 'zip_code', 'latitude', 'longitude',
                  'detailed_location', 'detailed_location_id', 'license_number', 'license_toggle',
                  'available_prices', 'amenities', 'images', 'charges', 'property_rental_created_at',
                  'property_rental_updated_at',
                    'checkin_checkout', 'created_at', 'updated_at'
                     )



