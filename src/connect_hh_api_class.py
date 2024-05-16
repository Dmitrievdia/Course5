from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HeadHunterParser(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который необходимо реализовать
    """

    def get_vacancies(self, keyword):
        url = 'https://api.hh.ru/vacancies'
        params = {'text': keyword, 'page': 0, 'per_page': 100}
        response = requests.get(url, params=params)
        return response.json()
