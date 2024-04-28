def calc_expected_payment(currency, payment_currency, payment_from, payment_to):
    if payment_currency != currency:
        expected_payment = None
    elif not payment_to:
        expected_payment = 1.2 * payment_from
    elif not payment_from:
        expected_payment = 0.8 * payment_to
    else:
        expected_payment = 0.5 * (payment_from + payment_to)
    return expected_payment
