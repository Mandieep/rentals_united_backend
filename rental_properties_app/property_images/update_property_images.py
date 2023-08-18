from rental_properties_app.models import Propertyimages


class UpdatePropertyImages():
    def update_property_images(self, property, property_info):
        images = property.get('Images')
        image_captions = property.get('ImageCaptions')

        image_captions_list = []
        if image_captions is not None:
            image_captions_list = image_captions.get('ImageCaption')

        if len(image_captions_list) < 1:
            image_captions_list = [image_captions_list]

        images_list = []
        if images is not None:
            images_list = images.get('Image')

        for image in images_list:
            image_type_id = image.get('@ImageTypeID')
            image_url = image.get('#text')
            image_reference_id = image.get('@ImageReferenceID')
            description = None
            language = None
            for image_cap in image_captions_list:
                if image_reference_id is not None and image_reference_id == image_cap.get('@ImageReferenceID') and image_cap.get('@LanguageID') == '1':
                    description = image_cap.get('#text')
                    language = 'English'
                    break

            print("--------image_url-----", image_url)
            print("--------image_type_id-----", image_type_id)
            print("--------description-----", description)
            print("--------language-----", language)

            property_image_obj = Propertyimages(image = image_url, image_type = image_type_id, image_descriptions = description,
                                                language = language, propertyinfo_id = property_info.id)
            property_image_obj.save()

        return True