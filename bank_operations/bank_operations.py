import json


class BankOperations:
    def __init__(self, filename):
        self.filename = filename
        self.operations = self.read_operations()

    def read_operations(self):
        """Читает операции из файла JSON и возвращает список словарей."""
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
