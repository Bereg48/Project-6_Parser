from manager.abs import SuperJobAPI, HeadHunterAPI


def user_interaction():
    search_query = input("Введите интересующую вакансии: ")
    search_query = SuperJobAPI.get_requests(search_query)
    print('Вакансии выгружены')
    prit = input("Если вам необходимо сортировать вакансии по зарплате нажмите один для выхода нажмите 2: ")
    if prit == 1:
        SuperJobAPI.sorting_from_descending(search_query)



    # SuperJobAPI.sorting_from_descending(search_query)
    # SuperJobAPI.filter_work_experience(search_query)

    # HeadHunterAPI.get_requests(search_query)
    # HeadHunterAPI.sorting_from_descending(search_query)
    # HeadHunterAPI.filter_work_experience(search_query)
    # HeadHunterAPI.merge(search_query)



    # if SuperJobAPI.modify_data(search_query) == "Страницы поиска SuperJobAPI собраны":
    #     print('Данные загружены')
    # else:
    #     print('Ошибка выгрузки данных')
    # SuperJobAPI.modify_data(search_query)
    # HeadHunterAPI.modify_data(search_query)
    # top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    # filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    # filtered_vacancies = filter_vacancies(hh_vacancies, superjob_vacancies, filter_words)
    #
    # if not filtered_vacancies:
    #     print("Нет вакансий, соответствующих заданным критериям.")
    #     return
    #
    # sorted_vacancies = sort_vacancies(filtered_vacancies)
    # top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    # print_vacancies(top_vacancies)


# if __name__ == "__main__":
#     user_interaction()
