from src.staticmetod import (get_company,
                             get_company_vacancies)
from config import config
import psycopg2
from src.utils import (create_list_vacs,
                       create_database,
                       create_tables,
                       save_to_table_vacs,
                       save_to_table_comps,
                       create_list_comps)
from src.class_DBManager import DBManager


def main():
    params = config()
    list_company = ['Тинькофф', 'Яндекс', 'Банк Открытие',
                    'ГК АГАТ', 'SOKOLOV', 'Арконт',
                    'Авиакомпания Победа', 'Аэрофлот',
                    'S7 Airlines', 'Автосалон CHERY']

    companies = get_company(list_company)
    vacancies = get_company_vacancies(companies)
    new_vacs = create_list_vacs(vacancies)
    new_comp = create_list_comps(companies)
    create_database('hh_data', params)
    create_tables('hh_data', params)
    save_to_table_comps(new_comp, 'hh_data', params)
    save_to_table_vacs(new_vacs, 'hh_data', params)

    db = DBManager()
    print("Список всех компаний и количествоо вакансий у каждой компании: ")
    for query in db.get_companies_and_vacancies_count('hh_data', params):
        print(f'Наименование компании: "{query[0]}" - открытых вакансий: {query[1]}')

    print('\nОбщий список вакансий')
    for query in db.get_all_vacancies('hh_data', params):
        print(f'Наименование компании: "{query[0]}".'
              f'Вакансия: {query[1]}. Зарплата от: {query[2]}.'
              f'Ссылка на вакансию: {query[3]} ')

    for query in db.get_avg_salary('hh_data', params):
        print(f'\nСредняя зарплата по вакансиям: "{query[0]}".')

    print('\nТоп-10 высокооплачиваемых вакансий: ')
    for query in db.get_vacancies_with_higher_salary('hh_data', params):
        print(f'Наименование компании: "{query[0]}".'
              f'Вакансия: {query[1]}. Зарплата от: {query[2]}.'
              f'Ссылка на вакансию: {query[3]} ')

    user_query = input("Введите интересующую вас вакансию: ").strip().lower()
    for query in db.get_vacancies_with_keyword('hh_data', params, user_query):
        if user_query in query[1]:
            print(f'Наименование компании: "{query[0]}".'
                  f' Вакансия: {query[1]}. Зарплата от: {query[2]}. '
                  f'Ссылка на вакансию: {query[3]} ')
        elif user_query not in query[1]:
            print("Извините, такой вакансии нет")


if __name__ == '__main__':
    main()
