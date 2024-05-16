import psycopg2

from config import config


def connection_to_data(vacancies_list):
    db_params = config()
    conn = psycopg2.connect(**db_params)

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS vacancies")
    cur.execute("DROP TABLE IF EXISTS companies")
    cur.execute("CREATE TABLE companies("
                "id int  PRIMARY KEY,"
                "company_name varchar(100))")

    cur.execute("CREATE TABLE vacancies("
                "company_id int REFERENCES companies(id),"
                "title varchar(100),"
                "city varchar(50),"
                "salary_from int,"
                "salary_to int,"
                "link varchar(100))")

    conn.commit()
    id_company = 0
    for company_dict in vacancies_list:
        company_name = list(company_dict.keys())[0]
        vacancies = company_dict[company_name]
        id_company += 1
        cur.execute(
            "INSERT INTO companies (id, company_name)"
            " VALUES (%s, %s) returning *", (id_company, company_name))
        for vacancy in vacancies:
            title = vacancy['title']
            city = vacancy['city']
            salary_from = vacancy['salary_from']
            salary_to = vacancy['salary_to']
            link = vacancy['link']
            cur.execute(
                "INSERT INTO vacancies (company_id, title, city, salary_from, salary_to, link)"
                " VALUES (%s, %s, %s, %s, %s, %s) returning *", (id_company, title, city, salary_from, salary_to, link))

    conn.commit()

    cur.close()
    conn.close()
