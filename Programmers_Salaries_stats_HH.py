import os
from itertools import chain
from dotenv import load_dotenv
import requests


def request_for_vacancies(keyword: str, user_agent_hh: str):
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': user_agent_hh}
    page = 0
    pages_number = 1
    response = []
    while page < pages_number:
        params = {'per_page': '20', 'period': 30, 'only_with_salary': 'true', 'page': page,
                  'text': keyword, 'area': '1', 'professional_role': '96'}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = page_payload['pages']
        page += 1
        response.append(page_payload['items'])
    return response


def sort_payments_by_keyword(response: dict, keywords: list):
    payments_sorted_by_keyword = {}
    vacancies_found = {}
    for keyword in keywords:
        payments_sorted_by_keyword[keyword] = [{'payment_from': item['salary']['from'],
                                                'payment_to': item['salary']['to'],
                                                'currency': item['salary']['currency']}
                                               for item in response[keyword]]
        vacancies_found[keyword] = len(payments_sorted_by_keyword[keyword])
    return payments_sorted_by_keyword, vacancies_found


def sort_salaries_by_keyword(payments_sorted_by_keyword: dict, keywords: list):
    salaries_sorted_by_keyword = {}
    for keyword in keywords:
        salaries_sorted_by_keyword[keyword] = []
        for item in payments_sorted_by_keyword[keyword]:
            if item['currency'] == 'RUR':
                if item['payment_from'] and item['payment_to']:
                    salaries_sorted_by_keyword[keyword].append(0.5 * (item['payment_from'] + item['payment_to']))
                elif item['payment_from'] and item['payment_to'] is None:
                    salaries_sorted_by_keyword[keyword].append(1.2 * item['payment_from'])
                elif item['payment_from'] is None and item['payment_to']:
                    salaries_sorted_by_keyword[keyword].append(0.8 * item['payment_to'])
    return salaries_sorted_by_keyword


def sort_average_salaries_by_keyword(keywords: list, salaries_sorted_by_keyword: dict, vacancies_found):
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


def get_average_salaries_sorted_by_programming_language_hh():
    load_dotenv()
    user_agent_hh = os.environ['USER_AGENT_HH']
    keywords = ['java', 'python', 'c', 'c#', 'c++', 'java_script', 'rust']
    average_salaries_sorted_by_keyword = {}
    try:
        response = {keyword: list(chain(*request_for_vacancies(keyword, user_agent_hh))) for keyword in keywords}
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



