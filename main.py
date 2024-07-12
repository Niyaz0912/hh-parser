from classes.engine import HH

"""В этом файле вам необходимо реализовать интерфейс взаимодействия с парсером через консоль
А именно
- 1 предложить пользователю выбрать вакансию для поиска;
- 2 спросить сколько вакансий просмотреть от 20 до 200 c шагом 20 вакансий 
(понадобится дополнительный параметр в __init__) который потом надо будет реализовать в теле метода get_request();
- 3 спросить нужна ли сортировка по зарплате;
- 4 спросить сколько отсортированных вакансий вывести;
- 5 добавить докстринги в файле engine.py;
- 6 (дополнительно) добавить возможные исключения.

Для того чтобы это все работало
вам будет необходимо несколько модифицировать код который находится в пакете classes внутри файла engine.py
"""


def main():
    # 1. Предложить пользователю выбрать вакансию для поиска
    vacancy_to_search = input("Введите название вакансии для поиска: ")

    # 2. Просмотреть количество вакансий
    num_of_vacancies = int(input("Сколько вакансий просмотреть (от 20 до 200 с шагом 20): "))

    # 3. Сортировка по зарплате
    sort_by_salary = input("Нужна ли сортировка по зарплате? (да/нет): ").lower()
    if sort_by_salary == "да":
        sort_type = input("Сортировать по возрастанию или убыванию зарплаты? (да/нет): ").lower()
        type_of_sort = True if sort_type == "да" else False
    else:
        type_of_sort = None

    # 4. Количество отсортированных вакансий для вывода
    num_sorted_vacancies = int(input("Введите количество отсортированных вакансий: "))

    hh = HH(vacancy_to_search)
    my_vacancies = hh.get_request()

    print(hh.make_json(vacancy_to_search, my_vacancies))

    if type_of_sort is not None:
        sorted_vacancies = hh.sorting(vacancy_to_search, type_of_sort, my_vacancies, num_sorted_vacancies)
        for vacancy in sorted_vacancies:
            print(vacancy)
    else:
        print("Сортировка не выбрана.")


if __name__ == "__main__":
    main()
