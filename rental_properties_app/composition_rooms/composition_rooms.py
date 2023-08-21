from rental_properties_app.models import CompositionRooms


class UpdateCompositionRooms():
    def update_composition_property_ids(self, comp_ids, property_id):
        db_comp_rooms = CompositionRooms.objects.filter(composition_id__in = comp_ids)
        update_list = []
        for single_obj in db_comp_rooms:
            db_property_id = single_obj.property_id
            if db_property_id == '' or db_property_id is None:
                single_obj.property_id = property_id
            elif (db_property_id != '' or db_property_id is not None) and (db_property_id == property_id or property_id in db_property_id):
                continue
            elif (db_property_id != '' or db_property_id is not None) and property_id not in db_property_id:
                single_obj.property_id = db_property_id +', '+ property_id
            update_list.append(single_obj)
        CompositionRooms.objects.bulk_update(update_list, ['property_id'], batch_size=1000)
        return True

    def update_composition_rooms(self, property, property_id):
        composition_room_ids = []
        comp_rooms_list = None
        comp_rooms_amenities = property.get('CompositionRoomsAmenities')
        if comp_rooms_amenities is not None:
            comp_rooms_list = comp_rooms_amenities.get('CompositionRoomAmenities')
        if comp_rooms_list is not None and comp_rooms_list != '':
            if type(comp_rooms_list) == dict:
                if comp_rooms_list.get('@CompositionRoomID') not in composition_room_ids:
                    composition_room_ids.append(comp_rooms_list.get('@CompositionRoomID'))
            else:
                composition_room_ids = [i.get('@CompositionRoomID') for i in comp_rooms_list
                                        if i.get('@CompositionRoomID') not in composition_room_ids]

            self.update_composition_property_ids(composition_room_ids, property_id)