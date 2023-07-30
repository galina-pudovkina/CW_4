from api.super_job_vacancy_api import SuperJobVacancyAPI
from api.hh_vacancy_api import HHVacancyAPI
from file_saver.json_saver import JsonSaver


class JobParser:
    """
    Класс для представления приложения
    """

    def __init__(self):
        self.json_saver = JsonSaver("vacancies.json")
        self.job_title = str(input("Введите название профессии: "))
        self.all_vacancies = []
        self.user_interaction()

    def hh_search_vacancy(self):
        """
        Метод для поиска вакансий на hh.ru
        """
        hh_vac = HHVacancyAPI(self.job_title)
        self.all_vacancies = hh_vac.get_formatted_vacancies()

    def sj_search_vacancy(self):
        """
        Метод для поиска вакансий на superjob
        """
        sj_vac = SuperJobVacancyAPI(self.job_title)
        self.all_vacancies = sj_vac.get_formatted_vacancies()

    def all_search_vacancy(self):
        """
        Метод для поиска вакансий c двух платформ
        """
        sj_vac = SuperJobVacancyAPI(self.job_title)
        hh_vac = HHVacancyAPI(self.job_title)
        self.all_vacancies = hh_vac.get_formatted_vacancies() + sj_vac.get_formatted_vacancies()

    def sorted_vacancies(self):
        """
        Метод для сортировки вакансий по зп
        """
        top_vacancy = int(input("Введите топ вакансий по зп: "))
        self.all_vacancies = sorted(self.all_vacancies, reverse=True)[:top_vacancy]

    def write_file(self):
        """
        Метод для записи полученных вакансий в файл
        """
        user_input = int(input("Хотите записать вакансии в файл? \n"
                               "Да 1\n"
                               "Нет 2\n"))

        while True:
            if user_input == 1:
                [self.json_saver.add_vacancy(vacancy) for vacancy in self.all_vacancies]
                break
            elif user_input == 2:
                break
            else:
                print("Введено неверное значение")

    def user_interaction(self):
        """
        Интерактив для пользователя
        """
        print("Для поиска с hh.ru Нажмите 1\n"
              "Для поиска с SuperJob 2\n"
              "Для поиска с hh.ru и SuperJob 3\n"
              "Для выхода 0")
        while True:
            user_input = int(input())
            if user_input == 1:
                self.hh_search_vacancy()
                self.sub_user_interaction()
                break
            elif user_input == 2:
                self.sj_search_vacancy()
                self.sub_user_interaction()
                break
            elif user_input == 3:
                self.all_search_vacancy()
                self.sub_user_interaction()
                break
            elif user_input == 0:
                exit()
            else:
                print("Введено неверное значение")
        self.write_file()

    def sub_user_interaction(self):
        """
        Подинтерактив для пользователя
        """
        user_input = int(input("Хотите ли отсортировать вакансии?\n"
                               "Да 1\n"
                               "Нет 2\n"))
        while True:
            if user_input == 1:
                self.sorted_vacancies()
                break
            elif user_input == 2:
                break
            else:
                print("Введено неверное значение")

        [print(vacancy) for vacancy in self.all_vacancies]
