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
