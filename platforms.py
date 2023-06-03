hh_api = HeadHunterAPI()
search_name = 'python'

result_1 = hh_api.get_vacancies(search_name)
vacancies = Vacancy(result_1[0]['title'], result_1[0]['link'], result_1[0]['salary'], result_1[0]['description'])
print(vacancies)