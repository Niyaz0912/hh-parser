import requests
import json
from abc import ABC, abstractmethod


class Engine(ABC):
    """Абстрактный класс, определяющий интерфейс для получения запроса"""

    @abstractmethod
    def get_request(self):
        """Абстрактный метод, который должен быть реализован в конкретных подклассах.
        Этот метод должен возвращать данные, полученные в результате запроса"""
        pass


class HH(Engine):
    """Класс для работы с API hh.ru и обработки вакансий. Здесь vacancies_all: список всех вакансий, полученных с hh.ru.
        vacancies_dicts: список словарей с информацией о вакансиях"""

    vacancies_all = []
    vacancies_dicts = []

    def __init__(self, vacancy):
        """Функция инициализирует объект класса HH с заданной вакансией, vacancy: Название вакансии,
        для которой будет выполняться поиск"""
        self.vacancy = vacancy

    def get_request(self):
        """Функция выполняет запрос к API hh.ru для получения вакансий.
        Возвращает список словарей с информацией о вакансиях"""
        for num in range(1):
            url = 'https://api.hh.ru/vacancies'
            vacancies_per_page = 20
            params = {
                'text': {self.vacancy},
                'areas': 113,
                'per_page': vacancies_per_page,
                'page': num,
                'only with salary': True
            }
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данны не получены!"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif info['found'] == 0:
                return "Нет вакансий"
            else:
                for vacancy in range(vacancies_per_page):
                    self.vacancies_all.append(vacancy)
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == 'RUR':
                        vacancy_dict = {'employer': info['items'][vacancy]['employer']['name'],
                                        'name': info['items'][vacancy]['name'],
                                        'url': info['items'][vacancy]['alternate_url'],
                                        'requirement': info['items'][vacancy]['snippet']['requirement'],
                                        'salary_from': info['items'][vacancy]['salary']['from'],
                                        'salary_to': info['items'][vacancy]['salary']['to']}
                        if vacancy_dict['salary_from'] is None:
                            vacancy_dict['salary_from'] = "не указано"
                        elif vacancy_dict['salary_to'] is None:
                            vacancy_dict['salary_to'] = "не указано"
                        self.vacancies_dicts.append(vacancy_dict)
        return self.vacancies_dicts

    @staticmethod
    def make_json(vacancy, vacancies_dicts):
        """Функция сохраняет список вакансий в JSON-файл.
        Здесь vacancy: название вакансии, для которой будет сохранен файл.
        vacancies_dicts: список словарей с информацией о вакансиях.
        Возвращает сообщение о сохранении файла"""
        with open(f"{vacancy}_hh_ru.json", 'w', encoding='utf-8') as file:
            json.dump(vacancies_dicts, file, indent=2, ensure_ascii=False)
        return f"Вакансии добавлены в файл: {vacancy}_hh_ru.json"

    @staticmethod
    def sorting(filename, type_of_sort, vacancies, num_of_vacancies=None):
        """Функция сортирует список вакансий по заработной плате и сохраняет отсортированный список в JSON-файл.
        filename: название файла, в который будут сохранены отсортированные вакансии.
        type_of_sort: определяет тип сортировки (True - по возрастанию, False - по убыванию).
        vacancies: список словарей с информацией о вакансиях.
        num_of_vacancies: количество вакансий, которые нужно вывести. Если не указано, выводятся все вакансии.
        Возвращает список отформатированных строк с информацией о вакансиях"""
        vacancies_list = []
        vacancies_sort = sorted(vacancies, key=lambda vacancy1: vacancy1['salary_from'], reverse=type_of_sort)
        for vacancy in vacancies_sort[:num_of_vacancies]:
            vacancies_list.append(f"""
        Наниматель: {vacancy['employer']}
        Вакансия: {vacancy['name']}
        Описание/Требования: {vacancy['requirement']}
        Заработная плата от {vacancy['salary_from']} до {vacancy['salary_to']}
        Ссылка на вакансию: {vacancy['url']}""")
        with open(f'{filename}_sorted_vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(vacancies_sort[:num_of_vacancies], file, indent=2, ensure_ascii=False)
        return vacancies_list
