def calc_expected_payment(currency: str, payment_currency: str, payment_from: int, payment_to: int):
    if payment_currency != currency:
        expected_payment = None
    elif not payment_to:
        expected_payment = 1.2 * payment_from
    elif not payment_from:
        expected_payment = 0.8 * payment_to
    else:
        expected_payment = 0.5 * (payment_from + payment_to)
    return expected_payment
