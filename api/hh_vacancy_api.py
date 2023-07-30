import requests

from exceptions import ParsingError
from api.parser import ParserAPI
from models.vacancy import Vacancy
from utils.currency_converter import get_currency_data


class HHVacancyAPI(ParserAPI):
    """
    Класс, наследующийся от абстрактного класса,
    для работы с платформой hh.ru
    """
    url = "https://api.hh.ru/vacancies"

    def __init__(self, keyword):
        self.keyword = keyword
        self.params = {
            'only_with_salary': True,
            "per_page": 100,
            "page": None,
            "text": keyword,
            "archived": False
        }
        self.vacancies = self.get_request()

    def get_request(self):
        """
        Метод для подключения к апи
        :return: список словарей json
        """
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус {response.status_code}")
        return response.json()["items"]

    def get_formatted_vacancies(self):
        """
        Метод для форматирования списка словарей с вакансиями
        :return: приведенный к нужному виду список словарей
        """
        formatted_vacancies = []
        for vacancy in self.vacancies:
            if self.keyword.lower() in vacancy["name"].lower():
                url = vacancy["alternate_url"]
                title = vacancy["name"]
                employer = vacancy['employer']['name']
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] is not None else 0
                if vacancy["salary"]["currency"].upper() not in ["RUR", "RUB"] and vacancy["salary"]["from"]:
                    salary_from *= get_currency_data(vacancy["salary"]["currency"])
                formatted_vacancies.append(Vacancy(title, url, salary_from, employer))
        return formatted_vacancies
