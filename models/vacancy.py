class Vacancy:
    """
    Класс для представления вакансии
    """
    vac_all = []

    def __init__(self, title, url, salary_from, employer):
        self.employer = employer
        self.salary_from = int(salary_from)
        self.url = url
        self.title = title
        self.vac_all.append({
            "Название профессии": self.title,
            "Работодатель": self.employer,
            "Зарплата от": self.salary_from,
            "Ссылка на вакансию": self.url
        })

    def __str__(self):
        return f"{self.title} {self.salary_from} ({self.url})"

    def __gt__(self, other):
        return self.salary_from > other.salary_from
