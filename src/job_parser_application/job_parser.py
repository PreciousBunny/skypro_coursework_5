import os
import sys
sys.path.append(os.getcwd())
from src.work_api.hh_api import HeadHunterAPI
from src.database.db_manager import DBManager
from src.job_parser_application.job_parser_meta import JobParserMeta
from config import EMPLOYERS_VACANCY_ID


class JobParser(metaclass=JobParserMeta):
    """
    Класс "создает" приложение по поиску вакансий.
    """
    hh_api = HeadHunterAPI()
    db_manager = DBManager()

    @classmethod
    def _user_interaction(cls):
        """
        Метод запускает взаимодействие с пользователем.
        """
        cls.db_manager.connect_db()
        cls.db_manager.delete_tables()
        cls.__get_database_in_all_vacancies()
        cls._get_menu()
        cls.db_manager.disable_db()

    @classmethod
    def __get_database_in_all_vacancies(cls):
        """
        Метод подключается к API сайта HeadHunter и получает список всех вакансий,
        которые записываются в базу данных.
        """
        id = 0

        for employer_name, employer_id in EMPLOYERS_VACANCY_ID.items():
            company_name = employer_name
            company_vacancies = cls.hh_api.get_vacancies(employer_id)
            for vacancy in company_vacancies:
                vacancy_name = vacancy["name"]
                vacancy_url = vacancy["alternate_url"]
                if vacancy.get("salary") and vacancy["salary"]["currency"] in ["RUR", "RUB"]:
                    vacancy_salary_from = int(vacancy["salary"]["from"]) if vacancy.get("salary") is not None and \
                                                                            vacancy[
                                                                                "salary"].get("from") is not None else 0
                    vacancy_salary_to = int(vacancy["salary"]["to"]) if vacancy.get("salary") is not None and vacancy[
                        "salary"].get("to") is not None else 0
                    vacancy_currency = "RUR"
                    vacancy_id = id + 1
                    id += 1

                    cls.db_manager.insert_into_all_vacancies(vacancy_id,
                                                             company_name,
                                                             vacancy_name,
                                                             vacancy_salary_from,
                                                             vacancy_salary_to,
                                                             vacancy_currency,
                                                             vacancy_url)

                    cls.db_manager.insert_into_company(vacancy_id,
                                                       company_name,
                                                       vacancy_name,
                                                       vacancy_salary_from,
                                                       vacancy_salary_to,
                                                       vacancy_currency,
                                                       vacancy_url)

    @classmethod
    def _get_menu(cls):
        """
        Метод отображает меню приложения для взаимодействия с пользователем.
        """
        print("\nВас приветствует обновленное приложение по поиску работы 2.0! Приятного поиска!")

        while True:
            print("\n1. Для получения списка всех компаний и количество вакансий у каждой компании")
            print("2. Для получения списка всех вакансий с указанием названия компании, названия вакансии, \n"
                  "зарплаты и ссылки на вакансию")
            print("3. Для получения средней зарплаты по вакансиям")
            print("4. Для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям")
            print("5. Для получения списка всех вакансий, в названии которых содержится введенное слово")
            print("6. Сохранить все вакансии в файл")
            print("0. Выход (exit)")
            menu_command_selection = input("\nПожалуйста, выберите один из предложенных вариантов:\n>_ ")

            if menu_command_selection == "1":
                cls._get_companies_and_vacancies_count()
            elif menu_command_selection == "2":
                cls._get_all_vacancies()
            elif menu_command_selection == "3":
                print("Средня зарплата в рублях:", end=" ")
                cls.get_avg_salary()
            elif menu_command_selection == "4":
                cls.get_vacancies_with_higher_salary()
            elif menu_command_selection == "5":
                keyword = input("Введите слово:\n>_ ")
                cls.get_vacancies_with_keyword(keyword)
            elif menu_command_selection == "6":
                cls.db_manager.save_vacancies_to_json_file('vacancies.json')
            elif menu_command_selection == "0":
                print("Спасибо, что воспользовались нашим новым приложением! Мы рады были Вам помочь!\n")
                break
            else:
                print("Некорректный выбор варианта. Попробуйте выбрать еще раз! (подсказка - введите число от 0 до 6)")

    @classmethod
    def _get_companies_and_vacancies_count(cls):
        """
        Метод выводит на экран список всех компаний и количество вакансий у каждой компании.
        """
        result_db = cls.db_manager._get_companies_and_vacancies_count()
        result_found = result_db.to_string(index=False)
        print(result_found)

    @classmethod
    def _get_all_vacancies(cls):
        """
        Метод выводит на экран список всех вакансий с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию.
        """
        result_db = cls.db_manager._get_all_vacancies()
        result_found = result_db.to_string(index=False)
        print(result_found)

    @classmethod
    def get_avg_salary(cls):
        """
        Метод выводит на экран среднюю зарплату по вакансиям.
        """
        print(cls.db_manager.get_avg_salary())

    @classmethod
    def get_vacancies_with_higher_salary(cls):
        """
        Метод выводит на экран список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        result_db = cls.db_manager.get_vacancies_with_higher_salary()
        result_found = result_db.to_string(index=False)
        print(result_found)

    @classmethod
    def get_vacancies_with_keyword(cls, keyword):
        """
        Метод выводит на экран список всех вакансий, в названии которых содержится введенное слово.
        """
        result_db = cls.db_manager.get_vacancies_with_keyword(keyword)
        result_found = result_db.to_string(index=False)
        print(result_found)
