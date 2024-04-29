import requests
import logging
from Common_functions import calc_expected_payment


logger = logging.getLogger('logger')


def request_vacancies_sj(app_secret_key_sj: str, language: str) -> (list, int):
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': f'{app_secret_key_sj}'}
    page = 0
    not_last_page = True
    vacancies_per_page = 100
    profession_number_sj = 48
    vacancy_lifetime_sj = 0
    vacancies = []
    vacancies_amount = 0
    logger.info(f'Requesting API HH for {language} vacancies')
    while not_last_page:
        params = {'catalogues': profession_number_sj, 'keyword': language, 'count': f'{vacancies_per_page}',
                  'period': vacancy_lifetime_sj, 'page': page}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        vacancies_amount = page_payload['total']
        vacancies.extend(page_payload['objects'])
        page += 1
        not_last_page = page_payload['more']
    return vacancies, vacancies_amount


def calculate_average_salary_sj(vacancies: list) -> (int, int):
    currency = 'rub'
    expected_salaries = []
    for vacancy in vacancies:
        payment_from = vacancy['payment_from']
        payment_to = vacancy['payment_to']
        payment_currency = vacancy['currency']
        expected_payment = calc_expected_payment(currency, payment_currency, payment_from, payment_to)
        if expected_payment:
            expected_salaries.append(expected_payment)
    vacancies_processed = len(expected_salaries)
    if vacancies_processed:
        average_salary = int(round(sum(expected_salaries) / vacancies_processed, 0))
    else:
        average_salary = 'n/d'
    return average_salary, vacancies_processed


def get_vacancies_statistics_sj(app_secret_key_sj: str, languages: tuple) -> dict:
    hr_statistics_sj = {}
    for language in languages:
        vacancies, vacancies_amount = request_vacancies_sj(app_secret_key_sj, language)
        average_salary, vacancies_processed = calculate_average_salary_sj(vacancies)
        hr_statistics_sj[language] = {'vacancies_amount': vacancies_amount,
                                      'vacancies_processed': vacancies_processed,
                                      'average_salary': average_salary}
    return hr_statistics_sj
