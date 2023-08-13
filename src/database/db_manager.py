import os
import sys
sys.path.append(os.getcwd())
from src.database.mixin_connect_db import MixinConnectDB
from src.database.read_queries_sql import read_queries_sql
import json
import pandas as pd


class MixinSaveJsonFile:
    """
    Миксин класс предоставляет метод для сохранения данных о вакансиях в JSON файл.
    """

    def save_vacancies_to_json_file(self, filename) -> bool:
        """
        Метод для сохранения данных о вакансиях в JSON файл.
        """
        vacancies = self._get_all_vacancies()

        if vacancies is None or vacancies.empty:
            print("No vacancies found to save to the JSON file.")
            return False
        try:
            vacancies_list = vacancies.to_dict(orient='records')
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(vacancies_list, json_file, indent=4, ensure_ascii=False)
            print(f"Vacancies are successfully saved to {filename}.")
            return True
        except Exception as ex:
            print(f"Error occurred while saving vacancies to {filename}: {ex}")
            return False


class DBManager(MixinConnectDB, MixinSaveJsonFile):
    """
    Класс DBManager подключается к базе данных PostgreSQL и работает с его данными.
    """
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    def __init__(self) -> None:
        """
        Создает экземпляр класса DBManager.
        """
        self.connected = None
        self.queries_sql = read_queries_sql()

    def _execute_query(self, query, params=None):
        """
        Метод для выполнения SQL-запросов к базе данных.
        """
        try:
            with self.connected:
                with self.connected.cursor() as cursor:
                    cursor.execute(query, params)
        except Exception as ex:
            print("Error executing query:", ex)

    def _description_query(self, query, params=None, fetch=False):
        """
        Метод для выполнения описательных SQL-запросов к базе данных.
        """
        try:
            with self.connected.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    result = cursor.fetchall()
                    columns = [desc[0] for desc in cursor.description]
                    return pd.DataFrame(result, columns=columns)
        except Exception as ex:
            print("Error executing query:", ex)
            return None

    def _create_table_all_vacancies(self) -> None:
        """
        Метод создает общую таблицу вакансий.
        """
        query = self.queries_sql["Создание общей таблицы вакансий"]
        self._execute_query(query)

    def _create_table_company(self, company_name) -> None:
        """
        Метод создает таблицу компании с вакансиями.
        """
        query = self.queries_sql["Создание таблицы компании с вакансиями"].replace("{company_name}", company_name)
        self._execute_query(query)

    def delete_tables(self) -> None:
        """
        Метод удаляет все таблицы базы данных.
        """
        query = self.queries_sql["Удаление всех таблиц"]
        self._execute_query(query)

    def insert_into_all_vacancies(self, id, company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to,
                                  vacancy_currency, vacancy_url):
        """
        Метод добавляет вакансии в общую таблицу вакансий.
        """
        self._create_table_all_vacancies()

        query = self.queries_sql["Добавление вакансии в общую таблицу вакансий"]
        params = (id, company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
        self._execute_query(query, params)

    def insert_into_company(self, vacancy_id, company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to,
                            vacancy_currency, vacancy_url):
        """
        Метод добавляет вакансии в таблицу компании.
        """
        self._create_table_company(company_name)

        query = self.queries_sql["Добавление вакансии в таблицу компании "].replace("{company_name}", company_name)
        params = (vacancy_id, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
        self._execute_query(query, params)

    def _get_companies_and_vacancies_count(self):
        """
        Метод получает список всех компаний и количество вакансий у каждой компании.
        """
        query = self.queries_sql["Выбор списка всех компаний и количество вакансий у них"]
        return self._description_query(query, fetch=True)

    def _get_all_vacancies(self):
        """
        Метод получает список всех вакансий с указанием названия компании, названия вакансии,
         а так же зарплаты и ссылки на вакансию.
        """
        query = self.queries_sql[
            "Выбор списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию"]
        return self._description_query(query, fetch=True)

    def get_avg_salary(self):
        """
        Метод получает среднюю зарплату по вакансиям.
        """
        query = self.queries_sql["Выбор средней зарплаты по вакансиям"]
        result = self._description_query(query, fetch=True)
        return f"от {result.iloc[0]['avg_salary_from']} до {result.iloc[0]['avg_salary_to']}" if not result.empty else None

    def get_vacancies_with_higher_salary(self):
        """
        Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()

        if avg_salary is not None:
            query = self.queries_sql["Выбор списка всех вакансий, у которых зарплата выше средней по всем вакансиям"]
            return self._description_query(query, fetch=True)
        return None

    def get_vacancies_with_keyword(self, keyword):
        """
        Метод получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        query = self.queries_sql["Выбор списка всех вакансий, в названии которых содержатся переданные в метод слова"]
        params = ('%' + keyword + '%',)
        return self._description_query(query, params=params, fetch=True)
