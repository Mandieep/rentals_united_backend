from rental_properties_app.models import Propertycharges


class UpdateChargeProfile():
    def update_charge_profile(self, property, property_info_obj):
        deposit = property.get('Deposit')
        deposit_type_id = deposit.get('@DepositTypeID')
        deposit_type_amount = deposit.get('#text')
        security_deposit = property.get('SecurityDeposit')
        security_deposit_type_id = security_deposit.get('@DepositTypeID')
        security_deposit_type_amount = security_deposit.get('#text')
        charge_profiles = property.get('ChargeProfiles')
        charge_profile = charge_profiles.get('ChargeProfile')
        print("---------------chrage_profile------------", charge_profile)
        additional_fee = charge_profile.get('ApplicableAdditionalFee')

        if additional_fee is None:
            additional_fee = []
        elif type(additional_fee) != list:
            additional_fee = [additional_fee]

        for add_fee in additional_fee:
            optional = add_fee.get('@Optional')
            optional_value = 0
            if optional == 'true':
                optional_value = 1

            value = add_fee.get('Value')
            name = add_fee.get('@Name')
            calculation_type = add_fee.get('@DiscriminatorID')
            extra_charge_type = add_fee.get('@FeeTaxType')
            kind = 'Fee'
            if extra_charge_type in ['1','2','3','4','5']:
                kind = 'Tax'

            collection_time = add_fee.get('@CollectTime')
            applied_to = []
            applicable_info = add_fee.get('ApplicableTo')
            fee_names = applicable_info.get('FeeNames')
            rent = applicable_info.get('Rent')
            if rent == 'true':
                applied_to = ['Rent']
            if fee_names is not None:
                applied_to.extend(fee_names.get('FeeName'))
            if len(applied_to) < 1:
                applied_to = None
            else:
                applied_to = str(applied_to)[1:-1]

            property_charges_obj = Propertycharges(kind = kind, calculation_type_id = calculation_type, collection_time_id = collection_time,
                                                value = value, is_optional = optional_value, name = name, applied_to = applied_to,
                                                down_payment_type_id = deposit_type_id, security_deposit_type_id = security_deposit_type_id,
                                                down_payment_amount = deposit_type_amount, extra_charge_type_id = extra_charge_type,
                                                security_deposit_amount = security_deposit_type_amount, propertyinfo_id = property_info_obj.id)
            property_charges_obj.save()

        return True