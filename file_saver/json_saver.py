import json


class JsonSaver:
    """
    Класс определяющий методы для добавления вакансий в файл
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        """
        Метод для добавдения вакансии в файл
        """
        vacancy_dict = {
            "Название профессии": vacancy.title,
            "Работодатель": vacancy.employer,
            "Зарплата от": vacancy.salary_from,
            "Ссылка на вакансию": vacancy.url
        }
        with open(self.file_path, "a", encoding="utf-8") as file:
            json.dump(vacancy_dict, file, indent=4, ensure_ascii=False)
            file.write("\n")
