import os
import math
import requests
from itertools import chain
from dotenv import load_dotenv


def request_for_vacancies(app_secret_key: str, keyword: str):
    url = '	https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': f'{app_secret_key}'}
    page = 0
    pages_number = 1
    response = []
    count = 100
    while page < pages_number:
        params = {'catalogues': 48, 'keyword': keyword, 'count': f'{count}', 'period': 0, 'page': page}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = math.ceil(page_payload['total'] / count)
        page += 1
        response.append(page_payload['objects'])
    return response


def sort_payments_by_keyword(response: dict, keywords: list):
    payments_sorted_by_keyword = {}
    vacancies_found = {}
    for keyword in keywords:
        payments_sorted_by_keyword[keyword] = [{'payment_from': item['payment_from'],
                                                'payment_to': item['payment_to'],
                                                'currency': item['currency']}
                                               for item in response[keyword]]
        vacancies_found[keyword] = len(payments_sorted_by_keyword[keyword])
    return payments_sorted_by_keyword, vacancies_found


def sort_salaries_by_keyword(payments_sorted_by_keyword: dict, keywords: list):
    salaries_sorted_by_keyword = {}
    for keyword in keywords:
        salaries_sorted_by_keyword[keyword] = []
        for item in payments_sorted_by_keyword[keyword]:
            if item['currency'] == 'rub':
                if item['payment_from'] > 0 and item['payment_to'] > 0:
                    salaries_sorted_by_keyword[keyword].append(0.5 * (item['payment_from'] + item['payment_to']))
                elif item['payment_from'] > 0 and item['payment_to'] == 0:
                    salaries_sorted_by_keyword[keyword].append(1.2 * item['payment_from'])
                elif item['payment_from'] == 0 and item['payment_to'] > 0:
                    salaries_sorted_by_keyword[keyword].append(0.8 * item['payment_to'])
    return salaries_sorted_by_keyword


def sort_average_salaries_by_keyword(keywords: list, salaries_sorted_by_keyword: dict, vacancies_found: dict):
    average_salaries = []
    for keyword in keywords:
        salaries = salaries_sorted_by_keyword[keyword]
        total_salaries = len(salaries)
        if total_salaries:
            average_salaries.append(round(sum(salaries) / total_salaries, 0))
        else:
            average_salaries.append('no vacancies found')
    average_salaries_sorted_by_keyword = {keyword: {'average_salary': average_salary,
                                                    'vacancies_processed': len(salaries_sorted_by_keyword[keyword]),
                                                    'vacancies_found': vacancies_found[keyword]}
                                          for keyword, average_salary
                                          in zip(keywords, average_salaries)}
    return average_salaries_sorted_by_keyword


def get_average_salaries_sorted_by_programming_language_sj():
    load_dotenv()
    keywords = ['java', 'python', 'c', 'c#', 'c++', 'java_script', 'rust']
    app_secret_key = os.environ['APP_SECRET_KEY_SJ']
    average_salaries_sorted_by_keyword = {}
    try:
        response = {keyword: list(chain(*request_for_vacancies(app_secret_key, keyword))) for keyword in keywords}
        payments_sorted_by_keyword, vacancies_found = sort_payments_by_keyword(response, keywords)
        salaries_sorted_by_keyword = sort_salaries_by_keyword(payments_sorted_by_keyword, keywords)
        average_salaries_sorted_by_keyword = (
            sort_average_salaries_by_keyword(keywords, salaries_sorted_by_keyword, vacancies_found)
        )
    except requests.ConnectionError as error:
        print(error)
    except requests.HTTPError as error:
        print(error)
    return average_salaries_sorted_by_keyword

