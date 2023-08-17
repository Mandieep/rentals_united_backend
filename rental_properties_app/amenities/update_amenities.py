from rental_properties_app.models import Amenities


class UpdateAmenities():
    def update_property_ids(self, amenity_ids, property_id):
        db_amenities = Amenities.objects.filter(amenity_id__in = amenity_ids)
        update_list = []
        for single_obj in db_amenities:
            db_property_id = single_obj.property_id
            if db_property_id == '' or db_property_id is None:
                single_obj.property_id = property_id
            elif (db_property_id != '' or db_property_id is not None) and (db_property_id == property_id or property_id in db_property_id):
                continue
            elif (db_property_id != '' or db_property_id is not None) and property_id not in db_property_id:
                single_obj.property_id = db_property_id +', '+ property_id
            update_list.append(single_obj)
        Amenities.objects.bulk_update(update_list, ['property_id'], batch_size=1000)
        return True
