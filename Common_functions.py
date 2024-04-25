def calc_expected_payment(currency, payment_currency, payment_from, payment_to, expected_salaries):
    while True:
        if payment_currency != currency:
            break
        if not payment_to:
            expected_salaries.append(1.2 * payment_from)
            break
        if not payment_from:
            expected_salaries.append(0.8 * payment_to)
            break
        expected_salaries.append(0.5 * (payment_from + payment_to))
        break
    return expected_salaries
