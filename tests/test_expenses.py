import json
import pytest

from spendsense import expense_service


@pytest.fixture
def temporary_expenses(tmp_path, monkeypatch):
    """Replace the real expense database with a temporary test file."""

    test_file = tmp_path / "expenses.json"

    def load_test_expenses():
        if not test_file.exists():
            return []

        with open(test_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_test_expenses(expenses):
        with open(test_file, "w", encoding="utf-8") as file:
            json.dump(expenses, file)

    monkeypatch.setattr(
        expense_service,
        "load_expenses",
        load_test_expenses
    )

    monkeypatch.setattr(
        expense_service,
        "save_expenses",
        save_test_expenses
    )

    return test_file


def test_add_expense(temporary_expenses):

    expense = expense_service.add_expense(
        "2026-11-01",
        "food",
        "250",
        "Lunch"
    )

    assert expense["id"] == 1
    assert expense["category"] == "Food"
    assert expense["amount"] == "250.00"


def test_view_expenses(temporary_expenses):

    expense_service.add_expense(
        "2026-11-01",
        "Food",
        "250",
        "Lunch"
    )

    expenses = expense_service.view_expenses()

    assert len(expenses) == 1


def test_edit_expense(temporary_expenses):

    expense_service.add_expense(
        "2026-11-01",
        "Food",
        "250",
        "Lunch"
    )

    updated = expense_service.edit_expense(
        1,
        amount="300"
    )

    assert updated["amount"] == "300.00"


def test_delete_expense(temporary_expenses):

    expense_service.add_expense(
        "2026-11-01",
        "Food",
        "250",
        "Lunch"
    )

    expense_service.delete_expense(1)

    assert expense_service.view_expenses() == []


def test_invalid_amount():

    with pytest.raises(ValueError):

        expense_service.add_expense(
            "2026-11-01",
            "Food",
            "-100",
            "Invalid amount"
        )


def test_invalid_date():

    with pytest.raises(ValueError):

        expense_service.add_expense(
            "01-11-2026",
            "Food",
            "100",
            "Invalid date"
        )


def test_nonexistent_expense(temporary_expenses):

    with pytest.raises(ValueError):

        expense_service.edit_expense(
            999,
            amount="100"
        )


def test_month_filter(temporary_expenses):

    expense_service.add_expense(
        "2026-11-01",
        "Food",
        "250",
        "November"
    )

    expense_service.add_expense(
        "2026-10-01",
        "Travel",
        "100",
        "October"
    )

    expenses = expense_service.get_expenses_by_month("2026-11")

    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"