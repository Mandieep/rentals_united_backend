from django.db import models


class Amenities(models.Model):
    amenity = models.CharField(max_length=255)
    amenity_id = models.IntegerField(null=True)
    property_id = models.TextField(null=True)

    class Meta:
        db_table = "property_amenities"

class CompositionRooms(models.Model):
    composition_room = models.CharField(max_length=255)
    composition_id = models.IntegerField(null=True)
    property_id = models.TextField(null=True)

    class Meta:
        db_table = "property_composition_rooms"

class Propertybasicinfo(models.Model):
    property_id = models.IntegerField(null=True)
    property_name = models.CharField(max_length=50)
    group = models.CharField(max_length=50, null=True)
    property_type = models.CharField(max_length=50)
    can_sleep_max = models.IntegerField(null=True)
    floor = models.IntegerField(null=True)
    size = models.FloatField(null=True)
    street = models.CharField(max_length=50, null=True)
    zip_code = models.CharField(null=True, max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    detailed_location = models.FloatField(null=True)
    detailed_location_id = models.IntegerField(null=True)
    license_number = models.CharField(max_length=50, null=True)
    license_toggle = models.BooleanField(default=False)
    property_rental_created_at = models.DateTimeField(null=True)
    property_rental_updated_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "property_basic_info"

class Propertydescription(models.Model):
    propertyinfo = models.ForeignKey(
        Propertybasicinfo, on_delete=models.CASCADE, null=True)
    language = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = "property_description"

class Propertyimages(models.Model):
    propertyinfo = models.ForeignKey(
        Propertybasicinfo, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="images/", max_length=255, null=True)
    image_type = models.CharField(max_length=50, null=True)
    image_descriptions = models.JSONField(null=True)
    language = models.CharField(max_length=50, null=True)
    class Meta:
        db_table = "property_images"

class Propertyavailabilityprices(models.Model):
    propertyinfo = models.ForeignKey(
        Propertybasicinfo, on_delete=models.CASCADE, null=True)
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)
    status = models.CharField(null=True, max_length=50)
    is_price = models.BooleanField(default=False)
    daily_price = models.FloatField(null=True)
    min_stay = models.IntegerField(null=True)
    extra_guest_price = models.FloatField(null=True)
    season = models.CharField(null=True, max_length=50)

    class Meta:
        db_table = "property_availability_prices"

class Propertycharges(models.Model):
    propertyinfo = models.ForeignKey(
        Propertybasicinfo, on_delete=models.CASCADE, null=True)
    kind = models.CharField(null=True, max_length=50)
    value = models.FloatField(null=True)
    is_optional = models.BooleanField(default=0)
    down_payment_amount = models.FloatField(null=True)
    security_deposit_amount = models.FloatField(null=True)
    name = models.CharField(null=True, max_length=50)
    applied_to = models.CharField(null=True, max_length=50)
    extra_charge_type_id = models.IntegerField(null=True)
    calculation_type_id = models.IntegerField(null=True)
    collection_time_id = models.IntegerField(null=True)
    down_payment_type_id = models.IntegerField(null=True)
    security_deposit_type_id = models.IntegerField(null=True)

    class Meta:
        db_table = "property_charges"

class Propertycheckincheckout(models.Model):
    propertyinfo = models.ForeignKey(
        Propertybasicinfo, on_delete=models.CASCADE, null=True)
    landlord_name = models.CharField(max_length=50, null=True)
    prior_days = models.IntegerField(default=0)
    landlord_email = models.EmailField(null=True)
    landlord_telephone = models.CharField(null=True, max_length=50)
    checkin_time_from = models.CharField(default="00:00", max_length=50)
    checkin_time_to = models.CharField(default="00:00", max_length=50)
    checkout_time = models.CharField(default="00:00", max_length=50)
    checkinplace = models.CharField(default="at_the_apartment", max_length=50)
    late_arrival_fee_from = models.CharField(default="00:00", max_length=50)
    late_arrival_fee_to = models.CharField(default="00:00", max_length=50)
    late_arrival_fee_cost = models.FloatField(default=0)
    early_departure_fee_from = models.CharField(default="00:00", max_length=50)
    early_departure_fee_to = models.CharField(default="00:00", max_length=50)
    early_departure_fee_cost = models.FloatField(default=0)

    class Meta:
        db_table = "property_checkin_checkout"
