from django.core.paginator import Paginator

class PropertiesListings():
    def listing_sorting(self, sort, table_property_data):
        """
        Sort the filtered data of property listing.

        Args:
            sort (dict): sort as a dict of params on behalf of sorting will be implemented.
            table_property_data (obj) : table_property_data as an obj of records after filtering.

        """
        created_at = sort.get('created_at')
        id = sort.get('id')

        if id is not None and created_at is None:
            order_by_param = 'id'
            if id == 'desc':
                order_by_param = '-id'
            table_property_data = table_property_data.order_by(
                order_by_param)

        elif id is not None and created_at is None:
            order_by_param = 'property_rental_created_at'
            if created_at == 'desc':
                order_by_param = '-property_rental_created_at'
            table_property_data = table_property_data.order_by(
                order_by_param)

        elif id is not None and created_at is not None:
            order_by_param1 = 'id'
            order_by_param2 = 'property_rental_created_at'
            if id == 'desc':
                order_by_param = '-id'
            if created_at == 'desc':
                order_by_param = '-property_rental_created_at'
            table_property_data = table_property_data.order_by(
                order_by_param1, order_by_param2)

        return table_property_data

    def listing_pagnation(self, table_property_data, limit, current_page):
        """
        Pagination on property listing.

        Args:
            limit (int): limit as a int of number of records to be shown.
            current_page (int): current_page as a int to show number of records od current page.
            table_property_data (obj) : table_property_data as an obj of records after sorting.

        """
        p = Paginator(table_property_data, limit)
        page_number = current_page if current_page else 1
        page_obj = p.get_page(page_number)
        table_property_data = page_obj.object_list
        return table_property_data, page_number