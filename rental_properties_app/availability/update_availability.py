from rental_properties_app.models import Propertyavailabilityprices
from rental_properties_app.rental_properties import pull_min_stay_details_from_ru, pull_property_prices_from_ru
import datetime


class UpdateAvailability():
    def update_availability(self, property_info_obj):
        min_stay_data = pull_min_stay_details_from_ru(property_info_obj.property_id)
        list_of_property_min_stay = min_stay_data.get('Pull_ListPropertyMinStay_RS')
        property_min_stay = list_of_property_min_stay.get('PropertyMinStay')
        min_stay_detials = property_min_stay.get('MinStay')
        if min_stay_detials is None:
            property_season = []
        elif type(min_stay_detials) != list:
            min_stay_detials = [min_stay_detials]

        prices_data = pull_property_prices_from_ru(property_info_obj.property_id)
        list_of_property_prices = prices_data.get('Pull_ListPropertyPrices_RS')
        property_prices = list_of_property_prices.get('Prices')
        property_season = property_prices.get('Season')
        if property_season is None:
            property_season = []
        elif type(property_season) != list:
            property_season = [property_season]

        for season in property_season:
            date_from = season.get('@DateFrom')
            date_to = season.get('@DateTo')
            daily_price = season.get('Price')
            extra_price = season.get('Extra')
            min_stay = None
            for min_stay_detail in min_stay_detials:
                min_stay_dateto = min_stay_detail.get('@DateTo')
                previous_date = datetime.datetime.strptime(min_stay_dateto, '%Y-%m-%d') - datetime.timedelta(days=1)
                if date_from == min_stay_detail.get('@DateFrom') and date_to == previous_date.strftime('%Y-%m-%d'):
                    min_stay = min_stay_detail.get('#text')
                    break

            availability_obj = Propertyavailabilityprices(date_from = date_from, date_to = date_to,
                                        status = 'available', is_price = 1, daily_price = daily_price,
                                        min_stay = min_stay, extra_guest_price = extra_price, season = None,
                                        propertyinfo_id = property_info_obj.id)
            availability_obj.save()

        return True