from rental_properties_app.models import Amenities, Propertybasicinfo
from rental_properties_app.rental_properties import pull_amenities, pull_list_of_properties_from_ru, pull_property_types
# from rental_properties_app.decorators import access_authorized_users_only
# from rental_properties_app.models import Propertyinfo
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rental_properties_app.response import Responsehandler
from logger_setup import logger

response_handler = Responsehandler()
# Create your views here.

@api_view(['GET'])
def sync_properties_from_rental(request):
    """
        For 'GET' request-> return records from property group table for specific group_id
        For 'POST' request-> update group, insert new record in pricing_data table if not exists and sync occupancy new prices.
    """
    try:
        if request.method == 'GET':
            data_dicts = pull_list_of_properties_from_ru()
            print('data_dict..............', data_dicts)

            for data_dict in data_dicts:

                # fetch values.
                list_of_details = data_dict.get('Pull_ListSpecProp_RS')
                property = list_of_details.get('Property')
                print('property...........', property)
                rental_united_id = property.get('rental_united_id', None)
                print('rental_united_id...........', rental_united_id)
                d_location = property.get('DetailedLocationID')
                print('d_location...........', d_location)
                coordinates = property.get('Coordinates')
                print('coordinates...........', coordinates)
                arrival_instructions = property.get('ArrivalInstructions')
                print('arrival_instructions...........', arrival_instructions)
                checkin_out = property.get('CheckInOut')
                print('checkin_out...........', checkin_out)
                deposit = property.get('Deposit')
                print('deposit...........', deposit)
                security_deposit = property.get('SecurityDeposit')
                print('security_deposit...........', security_deposit)
                # amenities = property.get('Amenities')
                # amenty = amenities.get('Amenity')
                # amenity_ids = [i.get('#text') for i in amenty]
                # print('amenity_ids...........', amenity_ids)
                descriptions = property.get('Descriptions')
                if descriptions == None:
                    description =None
                else:
                    description = descriptions.get('Description')
                if description == None:
                    final_desciption = None
                else:
                    final_desciption = description[0].get('Text') if type(description) == list else description.get('Text')
                print('final_desciption...........', final_desciption)
                # check if property name already exists or not, if not then create new property
                table_property_names = Propertybasicinfo.objects.all().values_list('property_name', flat=True)
                if property in table_property_names:
                    response_dict = response_handler.msg_response(
                        'Property name already exists', 422)
                    return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:
                    property_type_dict = pull_property_types()
                    amenities_dict = pull_amenities()
                    print('property_type_dict.............', property_type_dict)
                    print('amenities_dict.............', amenities_dict)
                    prop_types_rs = property_type_dict.get('Pull_ListPropTypes_RS')
                    property_types = prop_types_rs.get('PropertyTypes')
                    property_type = property_types.get('PropertyType')
                    property_type_name = [i.get('#text') for i in property_type if i.get('@PropertyTypeID') == property.get('PropertyTypeID')]
                    property_info = Propertybasicinfo(
                        property_name=property.get('Name'), property_type=property_type_name[0],
                        can_sleep_max=property.get('CanSleepMax'), floor=property.get('Floor'),
                        size=property.get('Space'), street=property.get('Street'), zip_code=property.get('ZipCode'),
                        longitude=coordinates.get('Longitude'), latitude=coordinates.get('Latitude'),
                        detailed_location=d_location.get('#text'),
                        detailed_location_id=d_location.get('@TypeID'),
                        license_number=property.get('LicenseNumber'), license_toggle=1)
                    property_info.save()
                    logger.info(
                        f"Property basic info saved in database successfully.")
                break

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
            print('amenities_dict.............', amenities_dict)
            amenities_rs = amenities_dict.get('Pull_ListAmenities_RS')
            amenities = amenities_rs.get('Amenities')
            amenity_list = amenities.get('Amenity')
            amenity_instances = []
            for amenity in amenity_list:
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
