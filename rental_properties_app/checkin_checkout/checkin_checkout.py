from rental_properties_app.models import Propertycheckincheckout


class CheckinCheckout():
    def save_checkin_checkout(self, basic_info_db_obj, property):
        arrival_instructions = property.get('ArrivalInstructions')
        checkinout = property.get('CheckInOut')
        if arrival_instructions is not None:
            landlord_name = arrival_instructions.get('Landlord')
            landlord_email = arrival_instructions.get('Email')
            landlord_telephone = arrival_instructions.get('Phone')
        else:
            landlord_name = landlord_email = landlord_telephone = None

        if checkinout.get('LateArrivalFees') is not None:
            late_arival_fees = checkinout.get('LateArrivalFees')
            late_arrival_fee = late_arival_fees.get('LateArrivalFee')
            late_arrival_fee_from = late_arrival_fee.get('@From')
            late_arrival_fee_to = late_arrival_fee.get('@To')
            late_arrival_fee_cost = late_arrival_fee.get('#text')
        else:
            late_arrival_fee_from = late_arrival_fee_to = "00:00"
            late_arrival_fee_cost = 0

        if checkinout.get('EarlyDepartureFees') is not None:
            early_depart_fees = checkinout.get('EarlyDepartureFees')
            early_depart_fee = early_depart_fees.get('EarlyDepartureFee')
            early_depart_fee_from = early_depart_fee.get('@From')
            early_depart_fee_to = early_depart_fee.get('@To')
            early_depart_fee_cost = early_depart_fee.get('#text')
        else:
            early_depart_fee_from = early_depart_fee_to = "00:00"
            early_depart_fee_cost = 0


        propertycheckincheckoutobj = Propertycheckincheckout(
                                propertyinfo=basic_info_db_obj,
                                landlord_name=landlord_name,
                                landlord_email=landlord_email,
                                landlord_telephone=landlord_telephone,
                                checkin_time_from=checkinout.get('CheckInFrom'),
                                checkin_time_to=checkinout.get('CheckInTo'),
                                checkout_time=checkinout.get('CheckOutUntil'),
                                checkinplace=checkinout.get('Place'),
                                late_arrival_fee_from=late_arrival_fee_from,
                                late_arrival_fee_to=late_arrival_fee_to,
                                late_arrival_fee_cost=late_arrival_fee_cost,
                                early_departure_fee_from=early_depart_fee_from,
                                early_departure_fee_to=early_depart_fee_to,
                                early_departure_fee_cost=early_depart_fee_cost,
                                prior_days=arrival_instructions.get('DaysBeforeArrival'),)
        propertycheckincheckoutobj.save()
