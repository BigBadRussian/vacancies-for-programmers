import requests
import logging


def request_vacancies(language: str, user_agent_hh: str):
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': user_agent_hh}
    page = 0
    pages_number = 1
    vacancies_per_page = 100
    profession_number_hh = '96'
    vacancy_lifetime_hh = 30
    searching_area_hh = '1'
    vacancies = []
    vacancies_amount = 0
    while page < pages_number:
        params = {'per_page': vacancies_per_page, 'period': vacancy_lifetime_hh, 'page': page,
                  'text': language, 'area': searching_area_hh, 'professional_role': profession_number_hh}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = page_payload['pages']
        page += 1
        vacancies.extend(page_payload['items'])
        vacancies_amount = page_payload['found']
    response = vacancies, vacancies_amount
    logging.basicConfig(level=logging.INFO)
    logging.info('request HH API')
    return response


def calculate_expected_salaries(vacancies):
    currency = 'RUR'
    expected_salaries = []
    payments = []
    for vacancy in vacancies:
        if vacancy['salary']:
            payments.append(vacancy['salary'])
    for payment in payments:
        payment_from = payment['from']
        payment_to = payment['to']
        payment_currency = payment['currency']
        if payment_currency != currency:
            continue
        if payment_from and payment_to:
            expected_salaries.append(0.5 * (payment_from + payment_to))
            continue
        if payment_from:
            expected_salaries.append(1.2 * payment_from)
            continue
        if payment_to:
            expected_salaries.append(0.8 * payment_to)
    return expected_salaries


def calculate_average_salaries(expected_salaries):
    total_salaries = len(expected_salaries)
    if total_salaries:
        average_salary = round(sum(expected_salaries) / total_salaries, 0)
    else:
        average_salary = 'no vacancies found'
    return average_salary, total_salaries


def get_vacancies_statistics_hh(user_agent_hh, languages):
    expected_salaries = {}
    average_salaries = {}
    vacancies_amount = {}
    vacancies_processed = {}
    hr_statistics_hh = {}
    for language in languages:
        vacancies, vacancies_amount[language] = request_vacancies(language=language, user_agent_hh=user_agent_hh)
        expected_salaries[language] = calculate_expected_salaries(vacancies)
        average_salaries[language], vacancies_processed[language] = calculate_average_salaries(
            expected_salaries[language])
        hr_statistics_hh[language] = {'vacancies_amount': vacancies_amount[language],
                                      'vacancies_processed': vacancies_processed[language],
                                      'average_salary': average_salaries[language]}
    return hr_statistics_hh
