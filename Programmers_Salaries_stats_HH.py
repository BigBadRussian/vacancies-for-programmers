from itertools import chain
import requests


def request_vacancies(search_word: str, user_agent_hh: str):
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
                  'text': search_word, 'area': searching_area_hh, 'professional_role': profession_number_hh}
        page_response = requests.get(url=url, headers=headers, params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()
        pages_number = page_payload['pages']
        page += 1
        vacancies.append(page_payload['items'])
        vacancies_amount = page_payload['found']
    response = vacancies, vacancies_amount
    print('request HH')
    return response


def get_payments(hh_response_vacancies_amount: dict, search_words: list):
    payments = {}
    for search_word in search_words:
        payments[search_word] = []
        for item in hh_response_vacancies_amount[search_word]['vacancies']:
            if item['salary']:
                payments[search_word].append({'payment_from': item['salary']['from'],
                                              'payment_to': item['salary']['to'],
                                              'currency': item['salary']['currency']})
    return payments


def calculate_expected_rub_salaries(payments: dict, search_words: list, currency: str):
    expected_salaries = {}
    for search_word in search_words:
        expected_salaries[search_word] = []
        for payment in payments[search_word]:
            payment_from = payment['payment_from']
            payment_to = payment['payment_to']
            if payment['currency'] != currency:
                continue
            if payment_from and payment_to:
                expected_salaries[search_word].append(0.5 * (payment_from + payment_to))
                continue
            if payment_from:
                expected_salaries[search_word].append(1.2 * payment_from)
                continue
            if payment_to:
                expected_salaries[search_word].append(0.8 * payment_to)
    return expected_salaries


def calculate_average_salaries(search_words: list, expected_salaries: dict):
    average_salaries = []
    for search_word in search_words:
        salaries = expected_salaries[search_word]
        total_salaries = len(salaries)
        if total_salaries:
            average_salaries.append(round(sum(salaries) / total_salaries, 0))
        else:
            average_salaries.append('no vacancies found')
    return average_salaries


def get_vacancies_statistics_hh(user_agent_hh):
    search_words = ['rust', 'ruby', 'python', 'java_script', 'java', 'c', 'c++', 'c#', 'go']
    currency = 'RUR'
    hh_response_vacancies_amount = {}
    vacancies_statistics = {}
    try:
        for search_word in search_words:
            vacancies, vacancies_amount = request_vacancies(search_word, user_agent_hh)
            hh_response_vacancies_amount[search_word] = {'vacancies': list(chain(*vacancies)),
                                                         'vacancies_amount': vacancies_amount}
        payments = get_payments(hh_response_vacancies_amount, search_words)
        expected_salaries = calculate_expected_rub_salaries(payments, search_words, currency)
        average_salaries = calculate_average_salaries(search_words, expected_salaries)
        vacancies_statistics = {search_word: {'average_salary': average_salary,
                                              'vacancies_processed': len(expected_salaries[search_word]),
                                              'vacancies_amount': hh_response_vacancies_amount[search_word][
                                                  'vacancies_amount']}
                                for search_word, average_salary
                                in zip(search_words, average_salaries)}
    except requests.ConnectionError as error:
        print(error)
    except requests.HTTPError as error:
        print(error)
    return vacancies_statistics
