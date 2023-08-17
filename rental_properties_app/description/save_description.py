from rental_properties_app.models import Propertydescription


class SaveDescription():
    def save_description_in_db(self, final_desciption, property):
        if final_desciption is not None:
            property_desc_obj = Propertydescription(propertyinfo=property, language='English', description=final_desciption)
            property_desc_obj.save()