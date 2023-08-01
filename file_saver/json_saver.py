import json


class JsonSaver:
    """
    Класс определяющий методы для добавления вакансий в файл
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_vacancy(self, vacancy):
        """
        Метод для добавления вакансии в файл
        """

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancy, file, indent=4, ensure_ascii=False)
