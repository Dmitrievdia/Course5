import json
from abc import ABC, abstractmethod


class Saver(ABC):
    @abstractmethod
    def insert(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError


class JSONSaver(Saver):
    def __init__(self, file="/home/dia/PycharmProjects/Course5/data/vacancies.json"):
        self.file = file

    def insert(self, data):
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def delete(self):
        with open(self.file, 'w', encoding='utf-8') as f:
            pass
