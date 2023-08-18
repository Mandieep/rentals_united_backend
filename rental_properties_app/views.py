from rental_properties_app.amenities.update_amenities import UpdateAmenities
from rental_properties_app.availability.update_availability import UpdateAvailability
from rental_properties_app.checkin_checkout.checkin_checkout import CheckinCheckout
from rental_properties_app.description.save_description import SaveDescription
from rental_properties_app.models import Amenities, Propertybasicinfo
from rental_properties_app.rental_properties import pull_amenities, pull_list_of_properties_from_ru, pull_property_types
# from rental_properties_app.decorators import access_authorized_users_only
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rental_properties_app.response import Responsehandler
from logger_setup import logger
import datetime

response_handler = Responsehandler()
save_description_obj = SaveDescription()
checkin_checkout_obj = CheckinCheckout()

@api_view(['GET'])
def sync_properties_from_rental(request):
    """
        For 'GET' request-> return records from property group table for specific group_id
        For 'POST' request-> update group, insert new record in pricing_data table if not exists and sync occupancy new prices.
    """
    try:
        if request.method == 'GET':
            data_dicts = pull_list_of_properties_from_ru()

            for data_dict in data_dicts:

                # fetch values.
                list_of_details = data_dict.get('Pull_ListSpecProp_RS')
                property = list_of_details.get('Property')
                rental_united_id = property.get('rental_united_id', None)
                d_location = property.get('DetailedLocationID')
                coordinates = property.get('Coordinates')
                arrival_instructions = property.get('ArrivalInstructions')
                checkin_out = property.get('CheckInOut')
                deposit = property.get('Deposit')
                security_deposit = property.get('SecurityDeposit')

                # save amenities in db
                amenities = property.get('Amenities')
                amenty = None
                if amenities is not None:
                    amenty = amenities.get('Amenity')
                if amenty is not None:
                    if type(amenty)== list:
                        amenity_ids = [i.get('#text') for i in amenty]
                    else:
                        amenity_ids = [amenty.get('#text')]
                    update_amenity_obj = UpdateAmenities()
                    update_amenity_obj.update_property_ids(amenity_ids, data_dict.get('property_id'))

                # check if property name already exists or not, if not then create new property
                table_property_names = Propertybasicinfo.objects.all().values_list('property_name', flat=True)
                if property.get('Name') in table_property_names:
                    logger.info(
                        f"Duplicate property name.", property)
                    continue
                else:
                    property_type_dict = pull_property_types()
                    prop_types_rs = property_type_dict.get('Pull_ListPropTypes_RS')
                    property_types = prop_types_rs.get('PropertyTypes')
                    property_type = property_types.get('PropertyType')
                    property_type_name = [i.get('#text') for i in property_type if i.get('@PropertyTypeID') == property.get('PropertyTypeID')]
                    property_info = Propertybasicinfo(
                        property_id = data_dict.get('property_id'), property_name=property.get('Name'), property_type=property_type_name[0],
                        can_sleep_max=property.get('CanSleepMax'), floor=property.get('Floor'),
                        size=property.get('Space'), street=property.get('Street'), zip_code=property.get('ZipCode'),
                        longitude=coordinates.get('Longitude'), latitude=coordinates.get('Latitude'),
                        detailed_location=d_location.get('#text'),
                        detailed_location_id=d_location.get('@TypeID'),
                        license_number=property.get('LicenseNumber'), license_toggle=1)
                    property_info.save()
                    logger.info(
                        f"Property basic info saved in database successfully.")
                    availability_obj = UpdateAvailability()
                    availability_obj.update_availability(property_info)
                    logger.info(
                        f"Property availability saved in database successfully.")

                    # save description in db
                    basic_info_db_obj = Propertybasicinfo.objects.get(property_id = data_dict.get('property_id'))
                    descriptions = property.get('Descriptions')
                    final_description = None
                    if descriptions is not None:
                        description = descriptions.get('Description')

                    if description is not None:
                        if type(description) == list:
                            for desc in description:
                                if int(desc.get('@LanguageID')) == 1:
                                    final_description = desc.get('Text')
                                    break
                        else:
                            final_description = description.get('Text') if int(description.get('@LanguageID')) == 1 else None
                    save_description_obj.save_description_in_db(final_description, basic_info_db_obj)

                    # save checkin checkout in db.
                    checkin_checkout_obj.save_checkin_checkout(basic_info_db_obj, property)

            response_dict = response_handler.success_response(
                        True, 200)
            return Response(response_dict, status.HTTP_200_OK)

    except Exception as e:
        logger.exception(
            f"error in function sync_properties_from_rental")
        exception_dict = {"message": str(e), "status": 500}
        return Response(exception_dict, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def save_amenities_in_db(request):
    """
        For 'GET' request-> return records from property

    """
    try:
        if request.method == 'GET':
            amenities_dict = pull_amenities()
            amenities_rs = amenities_dict.get('Pull_ListAmenities_RS')
            amenities = amenities_rs.get('Amenities')
            amenity_list = amenities.get('Amenity')
            amenity_instances = []
            db_amenities = Amenities.objects.all()
            amenity_ids = [int(amenity.amenity_id) for amenity in db_amenities]
            for amenity in amenity_list:
                if int(amenity.get('@AmenityID')) in amenity_ids:
                    continue
                amenity_ins = Amenities(amenity_id = amenity.get('@AmenityID'), amenity = amenity.get('#text'))
                amenity_instances.append(amenity_ins)
            Amenities.objects.bulk_create(amenity_instances)

            response_dict = response_handler.success_response(
                        True, 200)
            return Response(response_dict, status.HTTP_200_OK)

    except Exception as e:
        logger.exception(
            f"error in function save_amenities_in_db")
        exception_dict = {"message": str(e), "status": 500}
        return Response(exception_dict, status.HTTP_500_INTERNAL_SERVER_ERROR)
