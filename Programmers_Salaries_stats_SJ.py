import os
import math
import requests
from itertools import chain
from Programmers_Salaries_stats_HH import calculate_average_salaries
from Programmers_Salaries_stats_HH import calculate_expected_rub_salaries


def request_vacancies(app_secret_key_sj: str, search_word: str):
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': f'{app_secret_key_sj}'}
    page = 0
    pages_number = 1
    vacancies_per_page = 100
    profession_number_sj = 48
    vacancy_lifetime_sj = 0
    response = []
    while page < pages_number:
        params = {'catalogues': profession_number_sj, 'keyword': search_word, 'count': f'{vacancies_per_page}',
                  'period': vacancy_lifetime_sj, 'page': page}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = math.ceil(page_payload['total'] / vacancies_per_page)
        page += 1
        response.append(page_payload['objects'])
    print('request SJ')
    return response


def get_vacancies_amount_and_payments(sj_response_vacancies: dict, search_words: list):
    payments = {}
    vacancies_amount = {}
    for search_word in search_words:
        payments[search_word] = [{'payment_from': item['payment_from'],
                                  'payment_to': item['payment_to'],
                                  'currency': item['currency']}
                                 for item in sj_response_vacancies[search_word]]
        vacancies_amount[search_word] = len(payments[search_word])
    return payments, vacancies_amount


def get_vacancies_statistics_sj():
    app_secret_key_sj = os.environ['APP_SECRET_KEY_SJ']
    search_words = ['rust', 'ruby', 'python', 'java_script', 'java', 'c', 'c++', 'c#', 'go']
    currency = 'rub'
    vacancies_statistics = {}
    sj_response_vacancies = {}
    try:
        for search_word in search_words:
            vacancies = list(chain(*request_vacancies(app_secret_key_sj, search_word)))
            sj_response_vacancies[search_word] = vacancies

        payments, vacancies_amount = get_vacancies_amount_and_payments(sj_response_vacancies, search_words)
        expected_salaries = calculate_expected_rub_salaries(payments, search_words, currency)
        average_salaries = calculate_average_salaries(search_words, expected_salaries)
        vacancies_statistics = {search_word: {'average_salary': average_salary,
                                              'vacancies_processed': len(expected_salaries[search_word]),
                                              'vacancies_amount': vacancies_amount[search_word]}
                                for search_word, average_salary in zip(search_words, average_salaries)}
    except requests.ConnectionError as error:
        print(error)
    except requests.HTTPError as error:
        print(error)
    return vacancies_statistics
