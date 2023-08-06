from src.work_api.abstract_api import AbstractAPI
import requests


class HeadHunterAPI(AbstractAPI):
    """
    Класс подключается к API сайта HeadHunter и получает вакансии.
    """
    url = "https://api.hh.ru/vacancies"

    def __init__(self, url, vacancies_count=50):
        """
        Инициализация класса HeadHunterAPI.
        """
        self._url = url
        self._vacancies_count = vacancies_count

    def get_vacancies(self, employer_id, page=1):
        """
        Метод для поиска вакансий через HeadHunter API.
        """
        params = {
            'employer_id': employer_id,
            'per_page': self._vacancies_count,
            'archived': False,
            'page': page,
        }

        result = requests.get(url=self._url, params=params)
        result_json = result.json()

        return result_json.get("items", [])

    def get_company_vacancies(self, employer_id):
        """
        Метод создает список с вакансиями на соответствующей странице.
        """
        vacancies = []
        for page in range(50):
            vacancies_page = self.get_vacancies(employer_id, page)
            if len(vacancies_page) == 0:
                break
            vacancies.extend(vacancies_page)

        return vacancies