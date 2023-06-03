from abc import ABC, abstractmethod
import os
from operator import itemgetter
import requests
import json

url_hh = 'https://api.hh.ru/vacancies'
url_sj = 'https://api.superjob.ru/2.0/vacancies/?t=4&count=100'
# search_query = input("Введите поисковый запрос: ")

API_KEY_SUPER_JOB = os.environ.get('API_KEY_SUPER_JOB')


class VacanciesGETClass(ABC):
    """ Класс получения вакансий с HeadHunter"""  # класс работы с API (HH, SJ)

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def modify_data(self):
        pass

    @abstractmethod
    def get_requests(self):
        pass

    @abstractmethod
    def sorting_from_descending(self):
        pass

    @abstractmethod
    def filter_work_experience(self):
        pass

    @abstractmethod
    def merge(self):
        pass


class SuperJobAPI(VacanciesGETClass):

    def __init__(self, search_query):
        self.params = {'town': 4,
                       'count': 100,
                       'keyword': search_query

                       }

    def get_requests(self, page: int = 0):
        # params = {'town': 4,
        #           'count': 100,
        #           'keyword': search_query
        #
        #           }
        headers = {'X-Api-App-Id': API_KEY_SUPER_JOB}
        response = requests.get(url_sj, self.params, headers=headers)
        return response.content.decode()

    for page in range(0, 1):
        json_obj = json.loads(get_requests(page))
        filename = '../data/vacancies_raw/SuperJob.json'
        with open(filename, mode='w', encoding='utf8') as f:
            f.write(json.dumps(json_obj, ensure_ascii=False, indent=4, separators=(",", ":")))

    print('Страницы поиска SuperJobAPI собраны')

    def modify_data(self):
        """Метод modify_data работает с пришедшими данными SuperJob.json, конвертирует в единый формат данных,
        приводит к единому формализованному формату и создает файл SuperJob_formalized.json"""

        for fl in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/SuperJob.json'.format(fl), encoding='utf8') as f:
                json_text = f.read()
                json_obj = json.loads(json_text)
                new_str = []
                for v in json_obj["objects"]:
                    name = v['profession']
                    salary_from = v['payment_from']
                    salary_to = v['payment_to']
                    requirement = v['vacancyRichText']
                    responsibility = v['candidat']
                    organization = v['firm_name']
                    experience = v['experience']['title']

                    formalized_dict = {
                        'name_vacancies': name,
                        'organization': organization,
                        'salary_from': salary_from,
                        'salary_to': salary_to,
                        'experience': experience,
                        'requirement': requirement,
                        'responsibility': responsibility,
                        'api': 'SuperJob'
                    }

                    new_str.append(formalized_dict)
                filename_dict = '../data/vacancies_raw/SuperJob_formalized.json'
                with open(filename_dict, mode='w', encoding='utf8') as f:
                    json.dump(new_str, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Страницы поиска SuperJobAPI форматированы')

    def sorting_from_descending(self):
        """Метод sorting_from_descending работает с пришедшими данными SuperJob_formalized.json, производит сортировку
        данных по зарплате от максимальной к минимальной, и создает файл SuperJob_formalized_sorted.json"""

        for flo in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/SuperJob_formalized.json'.format(flo), encoding='utf8') as file:
                json_text_sorted = file.read()
                json_obj_sorted = json.loads(json_text_sorted)
                json_obj_sorted_two = sorted(json_obj_sorted, key=itemgetter('salary_from'), reverse=True)
                filename_dict_sorted = '../data/vacancies_raw/SuperJob_formalized_sorted.json'
                with open(filename_dict_sorted, mode='w', encoding='utf8') as f:
                    json.dump(json_obj_sorted_two, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Данные файла SuperJob_formalized.json отсортированы по зарплате от максимальной к минимальной')

    def filter_work_experience(self):
        """Метод filter_work_experience работает с пришедшими данными SuperJob_formalized.json, производит фильтрацию
        данных по критерию experience, и создает файл SuperJob_formalized_filter.json"""

        for flo in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/SuperJob_formalized.json'.format(flo), encoding='utf8') as fil:
                json_text_filter = fil.read()
                json_obj_filter = json.loads(json_text_filter)
                filter_dict_experience = [user for user in json_obj_filter if user['experience'] == "Без опыта"]
                filename_dict_filter_experience = '../data/vacancies_raw/SuperJob_formalized_filter.json'
                with open(filename_dict_filter_experience, mode='w', encoding='utf8') as f:
                    json.dump(filter_dict_experience, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Данные файла SuperJob_formalized.json отфильтрованы исходя из отсутствия опыта работы')


class HeadHunterAPI(VacanciesGETClass):

    def __init__(self, json_obj):
        self.json_obj = json_obj

    def get_requests(self, page: int = 0):
        """
        Метод для получения страницы со списком вакансий.
        Аргументы:
            text - Текст фильтра
            area - Поиск осуществляется по вакансиям города Москвы
            page - Индекс страницы поиска на HH
            per_page - Кол-во вакансий на 1 странице
            only_with_salary - показатель вакансий только с указанием зарплаты
        """
        # Справочник для параметров GET-запроса
        params = {
            'text': search_query,
            'area': 1,
            'page': page,
            'per_page': 100,
            'only_with_salary': True

        }
        response = requests.get(url_hh, params)  # Посылаем запрос к API
        data = response.content.decode()
        return data

    for page in range(0, 1):
        json_obj = json.loads(get_requests(page))
        filename = '../data/vacancies_raw/HeadHunter.json'
        with open(filename, mode='w', encoding='utf8') as f:
            f.write(json.dumps(json_obj, ensure_ascii=False, indent=4, separators=(",", ":")))
            if len(json_obj["items"]) == 0:
                print("Нет вакансий, соответствующих заданным критериям.")

            print('Страницы поиска HeadHunter собраны')

    def modify_data(self):
        """Метод modify_data работает с пришедшими данными HeadHunter.json, конвертирует в единый формат данных,
        приводит к единому формализованному формату и создает файл HeadHunter_formalized.json"""

        for fl in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/HeadHunter.json'.format(fl), encoding='utf8') as f:
                json_text = f.read()
                json_obj = json.loads(json_text)

                new_str = []
                for v in json_obj['items']:
                    name = v['name']
                    salary_from = v['salary']['from']
                    salary_to = v['salary']['to']
                    requirement = v['snippet']['requirement']
                    responsibility = v['snippet']['responsibility']
                    organization = v['employer']['name']
                    experience = v['experience']['name']
                    if isinstance(salary_to, int):
                        salary_to = salary_to
                    else:
                        salary_to = 0

                    if isinstance(salary_from, int):
                        salary_from = salary_from
                    else:
                        salary_from = 0

                    formalized_dict = {
                        'name_vacancies': name,
                        'organization': organization,
                        'salary_from': salary_from,
                        'salary_to': salary_to,
                        'experience': experience,
                        'requirement': requirement,
                        'responsibility': responsibility,
                        'api': 'HeadHunter'
                    }

                    new_str.append(formalized_dict)

                filename_dict = '../data/vacancies_raw/HeadHunter_formalized.json'

                with open(filename_dict, mode='w', encoding='utf8') as f:
                    json.dump(new_str, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Страницы поиска HeadHunter форматированы')

    def sorting_from_descending(self):
        """Метод sorting_from_descending работает с пришедшими данными HeadHunter_formalized.json, производит сортировку
        данных по зарплате от максимальной к минимальной, и создает файл HeadHunter_formalized_sorted.json"""

        for flo in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/HeadHunter_formalized.json'.format(flo), encoding='utf8') as file:
                json_text_sorted = file.read()
                json_obj_sorted = json.loads(json_text_sorted)
                json_obj_sorted_two = sorted(json_obj_sorted, key=itemgetter('salary_from'), reverse=True)
                filename_dict_sorted = '../data/vacancies_raw/HeadHunter_formalized_sorted.json'
                with open(filename_dict_sorted, mode='w', encoding='utf8') as f:
                    json.dump(json_obj_sorted_two, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Данные файла HeadHunter_formalized.json отсортированы по зарплате от максимальной к минимальной')

    def filter_work_experience(self):
        """Метод filter_work_experience работает с пришедшими данными HeadHunter_formalized.json, производит фильтрацию
        данных по критерию experience, и создает файл HeadHunter_formalized_filter.json"""

        for flo in os.listdir('../data/vacancies_raw/'):
            with open('../data/vacancies_raw/HeadHunter_formalized.json'.format(flo), encoding='utf8') as fil:
                json_text_filter = fil.read()
                json_obj_filter = json.loads(json_text_filter)
                filter_dict_experience = [user for user in json_obj_filter if user['experience'] == "Нет опыта"]
                filename_dict_filter_experience = '../data/vacancies_raw/HeadHunter_formalized_filter.json'
                with open(filename_dict_filter_experience, mode='w', encoding='utf8') as f:
                    json.dump(filter_dict_experience, f, ensure_ascii=False, indent=4, separators=(",", ":"))
        print('Данные файла HeadHunter_formalized.json отфильтрованы исходя из отсутствия опыта работы')

    def merge(self):
        """Метод merge работает с обработанными данными, производит объединение данных
        и создает файл HeadHunter_formalized_filter.json"""

        file_list = ['../data/vacancies_raw/HeadHunter_formalized.json',
                     '../data/vacancies_raw/SuperJob_formalized.json']
        all_data_dict = []
        for json_file in file_list:
            with open(json_file, 'r+', encoding='utf8') as file:
                file_data = json.load(file)
                all_data_dict.append(file_data)
                with open('../data/vacancies_raw/Vacancies.json', "w", encoding='utf8') as outfile:
                    json.dump(all_data_dict, outfile, ensure_ascii=False, indent=4, separators=(",", ":"))


SuperJobAPI.get_requests(search_query)
SuperJobAPI.modify_data(search_query)
SuperJobAPI.sorting_from_descending(search_query)
SuperJobAPI.filter_work_experience(search_query)

HeadHunterAPI.get_requests(search_query)
HeadHunterAPI.modify_data(search_query)
HeadHunterAPI.sorting_from_descending(search_query)
HeadHunterAPI.filter_work_experience(search_query)
HeadHunterAPI.merge(search_query)
