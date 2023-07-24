import os
from abc import ABC, abstractmethod

import requests

import json


from exceptions import ParsingError


class VacancyAPI(ABC):
    @abstractmethod
    def get_vacancies(self):
        raise NotImplementedError("В дочернем классе должен быть переопределен метод get_vacancies")

    @abstractmethod
    def get_request(self):
        raise NotImplementedError("В дочернем классе должен быть переопределен метод get_request()")


class HHVacancyAPI(VacancyAPI):
    url = "https://api.hh.ru/vacancies"

    def __init__(self, keyword):

        self.params = {
            "per_page": 100,
            "page": None,
            "text": keyword,
            "archived": False
        }
        self.headers = {
            "User-Agent": "MyImportantApp 1.0"
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус {response.status_code}")
        return response.json()["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS"
        }

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["employer"],
                "title": vacancy["name"],
                "url": vacancy["apply_alternate_url"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy[
                    "payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None
            }

            if vacancy["currency"] in currencies:
                formatted_vacancy["currency"] = currencies[vacancy["currency"]]
            elif vacancy["currency"]:
                formatted_vacancy["currency"] = "RUR"
                formatted_vacancy["currency_value"] = 1
            else:
                formatted_vacancy["currency"] = None
                formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)
    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break


class SuperJobVacancyAPI(VacancyAPI):
    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archived": False
        }
        self.headers = {
            "X-Api-App-Id": os.getenv("SUPER_JOB_API_KEY")
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус {response.status_code}")
        return response.json()["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS"
        }

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy[
                    "payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None
            }

            if vacancy["currency"] in currencies:
                formatted_vacancy["currency"] = currencies[vacancy["currency"]]
            elif vacancy["currency"]:
                formatted_vacancy["currency"] = "RUR"
                formatted_vacancy["currency_value"] = 1
            else:
                formatted_vacancy["currency"] = None
                formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
