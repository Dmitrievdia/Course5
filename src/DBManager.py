import psycopg2

from config import config


class DBManager:
    """
    класс DBManager для работы с данными в БД
    """

    def __init__(self):
        db_params = config()
        self.conn = psycopg2.connect(**db_params)

    def get_companies_and_vacancies_count(self):
        """
        Функция получает список всех компаний и количество вакансий у каждой компании
        """
        cur = self.conn.cursor()
        cur.execute("""SELECT c.company_name, COUNT(v.company_id) as vacancies_count\n
                       FROM companies c
                       LEFT JOIN vacancies v ON c.id = v.company_id
                       GROUP BY c.company_name;""")
        self.conn.commit()
        return cur.fetchall()

    def get_all_vacancies(self):
        """
        Функция получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        cur = self.conn.cursor()
        cur.execute("""SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link
                       FROM companies c
                       JOIN vacancies v ON c.id = v.company_id;""")
        return cur.fetchall()

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям
        """
        cur = self.conn.cursor()
        cur.execute("""SELECT AVG(salary_from + salary_to) / 2
                       FROM vacancies""")
        return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        cur = self.conn.cursor()
        cur.execute(f"""SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link
                              FROM companies c
                              JOIN vacancies v ON c.id = v.company_id
                              WHERE ((v.salary_from +v.salary_to) / 2) > {self.get_avg_salary()} """)
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        """
        cur = self.conn.cursor()
        cur.execute(f"""SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link
                       FROM companies c
                       JOIN vacancies v ON c.id = v.company_id
                       WHERE v.title ILIKE '%{keyword}%' OR c.company_name ILIKE '%{keyword}%' """)
        return cur.fetchall()
