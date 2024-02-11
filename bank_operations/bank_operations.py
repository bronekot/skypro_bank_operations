import json
from datetime import datetime


class BankOperations:
    def __init__(self, filename):
        self.filename = filename
        self.operations = self.read_operations()

    def read_operations(self):
        """Читает операции из файла JSON и возвращает список словарей."""
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    @staticmethod
    def mask_identifier(identifier):
        """Маскирует номер карты или счета в зависимости от типа идентификатора."""
        digits = ''.join(filter(str.isdigit, identifier))
        if "Счет" in identifier:
            # Маскировка для счета, оставляем видимыми только последние 4 цифры
            return identifier.replace(digits, '**' + digits[-4:])
        else:
            # Маскировка для номера карты, оставляем видимыми первые 6 и последние 4 цифры
            masked_digits = f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
            return identifier.replace(digits, masked_digits)

    def filter_executed_operations(self):
        """Фильтрует и возвращает выполненные операции."""
        return [op for op in self.operations if 'state' in op and op['state'] == 'EXECUTED']

    def print_last_five_executed_operations(self):
        """Выводит последние 5 выполненных операций."""
        executed_operations = self.filter_executed_operations()
        # Сортировка операций по дате в убывающем порядке
        executed_operations.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

        # Вывод последних 5 операций
        for operation in executed_operations[:5]:
            date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
            description = operation['description']
            from_account = self.mask_identifier(operation['from']) if 'from' in operation else "Не указано"
            to_account = self.mask_identifier(operation['to']) if 'to' in operation else "Не указано"
            amount = operation['operationAmount']['amount']
            currency_name = operation['operationAmount']['currency']['name']
            print(f"{date} {description}\n{from_account} -> {to_account}\n{amount} {currency_name}\n")


if __name__ == "__main__":
    operations_filename = '../data/operations.json'
    bank_operations = BankOperations(operations_filename)
    bank_operations.print_last_five_executed_operations()
