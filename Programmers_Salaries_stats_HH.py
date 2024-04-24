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


def calculate_average_salaries(vacancies):
    currency = 'RUR'
    expected_salaries: list = []
    for vacancy in vacancies:
        if vacancy['salary']:
            payment_from = vacancy['salary']['from']
            payment_to = vacancy['salary']['to']
            payment_currency = vacancy['salary']['currency']
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


def get_vacancies_statistics_hh(user_agent_hh, languages):
    hr_statistics_hh = {}
    for language in languages:
        vacancies, vacancies_amount = request_vacancies(language, user_agent_hh)
        average_salary, vacancies_processed = calculate_average_salaries(vacancies)
        hr_statistics_hh[language] = {'vacancies_amount': vacancies_amount,
                                      'vacancies_processed': vacancies_processed,
                                      'average_salary': average_salary}
    return hr_statistics_hh
