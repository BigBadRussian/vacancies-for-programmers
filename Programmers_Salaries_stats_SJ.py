import requests
import logging


logger = logging.getLogger('logger')


def request_vacancies_sj(app_secret_key_sj: str, language: str):
    logger.info('Requesting API SJ')
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': f'{app_secret_key_sj}'}
    page = 0
    pages_number = 1
    vacancies_per_page = 100
    profession_number_sj = 48
    vacancy_lifetime_sj = 0
    vacancies = []
    while page < pages_number:
        params = {'catalogues': profession_number_sj, 'keyword': language, 'count': f'{vacancies_per_page}',
                  'period': vacancy_lifetime_sj, 'page': page}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = page_payload['more']
        page += 1
        vacancies.extend(page_payload['objects'])
    return vacancies


def calculate_average_salaries_sj(vacancies: list):
    currency = 'rub'
    expected_salaries = []
    for vacancy in vacancies:
        payment_from = vacancy['payment_from']
        payment_to = vacancy['payment_to']
        payment_currency = vacancy['currency']
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
    vacancies_processed = len(expected_salaries)
    if vacancies_processed:
        average_salary = round(sum(expected_salaries) / vacancies_processed, 0)
    else:
        average_salary = 'no vacancies found'
    return average_salary, vacancies_processed


def get_vacancies_statistics_sj(app_secret_key_sj, languages):
    hr_statistics_sj = {}
    for language in languages:
        vacancies = request_vacancies_sj(app_secret_key_sj, language)
        average_salary, vacancies_processed = calculate_average_salaries_sj(vacancies)
        hr_statistics_sj[language] = {'vacancies_amount': len(vacancies),
                                      'vacancies_processed': vacancies_processed,
                                      'average_salary': average_salary}
    return hr_statistics_sj
