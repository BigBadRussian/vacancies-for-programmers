from __future__ import print_function
from terminaltables import AsciiTable
from Programmers_Salaries_stats_HH import get_average_salaries_sorted_by_programming_language_hh
from Programmers_Salaries_stats_SJ import get_average_salaries_sorted_by_programming_language_sj


def build_table(hr_service_data: dict, title: str):
    languages = tuple(hr_service_data.keys())
    table_data = []
    column_titles = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_data.append(column_titles)
    for language in languages:
        row = [language, hr_service_data[language]['vacancies_found'], hr_service_data[language]['vacancies_processed'],
               hr_service_data[language]['average_salary']]
        table_data.append(row)
    table = AsciiTable(table_data, title)
    print(table.table)


def main():
    build_table(hr_service_data=get_average_salaries_sorted_by_programming_language_hh(), title='HeadHunter Moscow')
    build_table(hr_service_data=get_average_salaries_sorted_by_programming_language_sj(), title='SuperJob Moscow')


if __name__ == '__main__':
    main()
