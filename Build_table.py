from __future__ import print_function

import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
from Programmers_Salaries_stats_HH import get_vacancies_statistics_hh
from Programmers_Salaries_stats_SJ import get_vacancies_statistics_sj


def build_table(hr_service_statistics: dict, title: str):
    table_rows = []
    column_titles = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_rows.append(column_titles)
    for search_word, statistics in hr_service_statistics.items():
        row = [search_word]
        row.extend(list(statistics.values()))
        table_rows.append(row)
    table = AsciiTable(table_rows, title)
    return table.table


def main():
    load_dotenv()
    user_agent_hh = os.environ['USER_AGENT_HH']
    app_secret_key_sj = os.environ['APP_SECRET_KEY_SJ']
    print(build_table(hr_service_statistics=get_vacancies_statistics_hh(user_agent_hh),
                      title='HeadHunter Moscow'),
          build_table(hr_service_statistics=get_vacancies_statistics_sj(app_secret_key_sj),
                      title='SuperJob Moscow'))


if __name__ == '__main__':
    main()
