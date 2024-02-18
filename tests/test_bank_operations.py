import pytest
from bank_operations import BankOperations


@pytest.fixture
def bank_operations():
    # Подготовка тестовых данных
    test_data = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000",
            "description": "Перевод с карты на счет",
            "from": "MasterCard 9454780748494532",
            "to": "Счет 51958934737718181351",
            "operationAmount": {
                "amount": "56071.02",
                "currency": {
                    "name": "руб."
                }
            }
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2023-01-02T13:00:00.000",
            "description": "Перевод отменен",
            "from": "Visa 1234567890123456",
            "to": "Счет 98765432109876544564",
            "operationAmount": {
                "amount": "10000",
                "currency": {
                    "name": "руб."
                }
            }
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-01-03T14:30:00.000",
            "description": "Перевод с карты на карту",
            "from": "Visa 1234567890123456",
            "to": "MasterCard 6543210987654321",
            "operationAmount": {
                "amount": "20000",
                "currency": {
                    "name": "руб."
                }
            }
        }
    ]

    bo = BankOperations('data/operations.json')
    bo.operations = test_data  # Замена реальных данных на тестовые
    return bo


def test_mask_identifier_card(bank_operations):
    masked = bank_operations.mask_identifier("MasterCard 9454780748494532")
    assert masked == "MasterCard 9454 78** **** 4532"


def test_mask_identifier_account(bank_operations):
    masked = bank_operations.mask_identifier("Счет 51958934737718181351")
    assert masked == "Счет **1351"


def test_filter_executed_operations(bank_operations):
    filtered = bank_operations.filter_executed_operations()
    assert len(filtered) == 2  # Проверяем, что отфильтрованы только выполненные операции
