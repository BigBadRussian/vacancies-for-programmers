import requests
import logging


logger = logging.getLogger('logger')


def request_vacancies_hh(language: str, user_agent_hh: str):
    logger.info('Requesting API HH')
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
    return response


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


def calculate_average_salary_hh(vacancies):
    currency = 'RUR'
    expected_salaries: list = []
    for vacancy in vacancies:
        if not vacancy['salary']:
            continue
        payment_from = vacancy['salary']['from']
        payment_to = vacancy['salary']['to']
        payment_currency = vacancy['salary']['currency']
        calc_expected_payment(currency, payment_currency, payment_from, payment_to, expected_salaries)
    vacancies_processed = len(expected_salaries)
    if vacancies_processed:
        average_salary = round(sum(expected_salaries) / vacancies_processed, 0)
    else:
        average_salary = 'no vacancies found'
    return average_salary, vacancies_processed


def get_vacancies_statistics_hh(user_agent_hh, languages):
    hr_statistics_hh = {}
    for language in languages:
        vacancies, vacancies_amount = request_vacancies_hh(language, user_agent_hh)
        average_salary, vacancies_processed = calculate_average_salary_hh(vacancies)
        hr_statistics_hh[language] = {'vacancies_amount': vacancies_amount,
                                      'vacancies_processed': vacancies_processed,
                                      'average_salary': average_salary}
    return hr_statistics_hh
