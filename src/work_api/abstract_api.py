from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """
    Абстрактный класс для поиска вакансий через HeadHunter API.
    """

    @abstractmethod
    def get_vacancies(self, employer_id):
        """
        Метод для поиска вакансий через HeadHunter API.
        """
        pass