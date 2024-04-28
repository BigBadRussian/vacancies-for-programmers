from __future__ import print_function

import logging
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
from Programmers_Salaries_stats_HH import get_vacancies_statistics_hh
from Programmers_Salaries_stats_SJ import get_vacancies_statistics_sj


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('logger')


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
    logger.info('start')
    load_dotenv()
    user_agent_hh = os.environ['USER_AGENT_HH']
    app_secret_key_sj = os.environ['APP_SECRET_KEY_SJ']
    languages = ('python', 'javascript', 'java', 'c', 'c++', 'c#', 'ruby', 'rust', 'go', 'php')
    print(build_table(hr_service_statistics=get_vacancies_statistics_hh(user_agent_hh, languages),
                      title='HeadHunter Moscow'), '\n',
          build_table(hr_service_statistics=get_vacancies_statistics_sj(app_secret_key_sj, languages),
                      title='SuperJob Moscow'))


if __name__ == '__main__':
    main()
