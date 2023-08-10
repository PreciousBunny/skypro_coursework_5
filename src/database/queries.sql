-- Active: 1689901380539@@127.0.0.1@5432@hh_job_parser@public
--Создание общей таблицы вакансий
CREATE TABLE IF NOT EXISTS all_vacancies(
            id INTEGER PRIMARY KEY,
            company_name VARCHAR(128) NOT NULL,
            vacancy_name VARCHAR(128) NOT NULL,
            vacancy_salary_from INTEGER NOT NULL,
            vacancy_salary_to INTEGER NOT NULL,
            vacancy_currency VARCHAR(128),
            vacancy_url VARCHAR(255) NOT NULL
);

--Создание таблицы компании с вакансиями
CREATE TABLE IF NOT EXISTS {company_name}(
    id SERIAL PRIMARY KEY,
    vacancy_name VARCHAR(128) NOT NULL,
    vacancy_salary_from INTEGER NOT NULL,
    vacancy_salary_to INTEGER NOT NULL,
    vacancy_currency VARCHAR(128) NOT NULL,
    vacancy_url VARCHAR(255) NOT NULL,
    vacancy_id INTEGER REFERENCES all_vacancies (id) ON DELETE CASCADE
);

--Удаление всех таблиц
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

--Добавление вакансии в общую таблицу вакансий
INSERT INTO all_vacancies (id, company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
VALUES (%s, %s, %s, %s, %s, %s, %s);

--Добавление вакансии в таблицу компании 
INSERT INTO {company_name} (vacancy_id, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
VALUES (%s, %s, %s, %s, %s, %s);

--Выбор списка всех компаний и количество вакансий у них
SELECT company_name, 
    count(*) as vacancies_count
FROM all_vacancies
GROUP BY company_name
ORDER BY vacancies_count DESC;

--Выбор списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
SELECT 
    company_name, 
    vacancy_name, 
    vacancy_salary_from,
    vacancy_salary_to, 
    vacancy_currency, 
    vacancy_url
FROM all_vacancies;

--Выбор средний зарплаты по вакансиям
SELECT
    (SELECT round(avg(vacancy_salary_from)) 
        FROM all_vacancies WHERE vacancy_salary_from != 0) 
            as avg_salary_from,
    (SELECT round(avg(vacancy_salary_to)) 
        FROM all_vacancies WHERE vacancy_salary_to != 0) 
            as avg_salary_to

--Выбор списка всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT 
    company_name, 
    vacancy_name,  
    vacancy_salary_from,
    vacancy_salary_to, 
    vacancy_currency, 
    vacancy_url
FROM all_vacancies
WHERE vacancy_salary_from >(
    SELECT round(avg(vacancy_salary_from))
    FROM all_vacancies
    WHERE vacancy_salary_from != 0) 
        and vacancy_salary_to >(
    SELECT round(avg(vacancy_salary_to))
    FROM all_vacancies
    WHERE vacancy_salary_to != 0)
    ORDER BY vacancy_salary_from DESC, 
            vacancy_salary_to DESC;

--Выбор списка всех вакансий, в названии которых содержатся переданные в метод слова
SELECT 
    company_name, 
    vacancy_name, 
    vacancy_salary_from,
    vacancy_salary_to, 
    vacancy_currency, 
    vacancy_url
FROM all_vacancies
WHERE lower(vacancy_name) ILIKE %s
ORDER BY vacancy_salary_from DESC, 
        vacancy_salary_to DESC;