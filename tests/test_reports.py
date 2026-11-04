
import pytest

from spendsense.report_service import (
    generate_monthly_summary,
    get_top_five_expenses,
    compare_monthly_spending,
    get_previous_month
)


@pytest.fixture
def sample_expenses():
    return [
        {
            "id": 1,
            "date": "2026-11-01",
            "category": "Food",
            "amount": "4000.00",
            "note": "Groceries"
        },
        {
            "id": 2,
            "date": "2026-11-02",
            "category": "Travel",
            "amount": "2500.00",
            "note": "Bus tickets"
        },
        {
            "id": 3,
            "date": "2026-11-03",
            "category": "Shopping",
            "amount": "1000.00",
            "note": "Clothes"
        },
        {
            "id": 4,
            "date": "2026-10-01",
            "category": "Food",
            "amount": "3000.00",
            "note": "Groceries"
        },
        {
            "id": 5,
            "date": "2026-10-02",
            "category": "Travel",
            "amount": "2500.00",
            "note": "Bus"
        }
    ]


@pytest.fixture
def sample_budgets():
    return [
        {
            "month": "2026-11",
            "category": "Food",
            "amount": "5000.00"
        },
        {
            "month": "2026-11",
            "category": "Travel",
            "amount": "3000.00"
        },
        {
            "month": "2026-11",
            "category": "Shopping",
            "amount": "2000.00"
        }
    ]


def test_monthly_summary(
    sample_expenses,
    sample_budgets
):
    result = generate_monthly_summary(
        "2026-11",
        sample_expenses,
        sample_budgets
    )

    assert result["total_spent"] == 7500
    assert result["total_budget"] == 10000
    assert result["remaining"] == 2500


def test_category_summary(
    sample_expenses,
    sample_budgets
):
    result = generate_monthly_summary(
        "2026-11",
        sample_expenses,
        sample_budgets
    )

    food = result["categories"]["Food"]

    assert food["spent"] == 4000
    assert food["budget"] == 5000
    assert food["remaining"] == 1000


def test_top_five(sample_expenses):
    result = get_top_five_expenses(
        "2026-11",
        sample_expenses
    )

    assert result[0]["amount"] == "4000.00"
    assert len(result) == 3


def test_top_five_limit():
    expenses = [
        {
            "id": i,
            "date": "2026-11-01",
            "category": "Food",
            "amount": str(i * 100),
            "note": "Test"
        }
        for i in range(1, 10)
    ]

    result = get_top_five_expenses(
        "2026-11",
        expenses
    )

    assert len(result) == 5
    assert result[0]["amount"] == "900"


def test_month_comparison(sample_expenses):
    result = compare_monthly_spending(
        "2026-11",
        sample_expenses
    )

    food = result["categories"]["Food"]

    assert result["previous_month"] == "2026-10"
    assert food["previous_spending"] == 3000
    assert food["current_spending"] == 4000
    assert food["change"] == 1000


def test_percentage_change(sample_expenses):
    result = compare_monthly_spending(
        "2026-11",
        sample_expenses
    )

    food = result["categories"]["Food"]

    assert float(food["percentage_change"]) == pytest.approx(33.333333)


def test_previous_month_january():
    assert get_previous_month("2027-01") == "2026-12"


def test_previous_month_march():
    assert get_previous_month("2027-03") == "2027-02"


def test_empty_month():
    result = generate_monthly_summary(
        "2026-12",
        [],
        []
    )

    assert result["total_spent"] == 0
    assert result["total_budget"] == 0
    assert result["categories"] == {}


def test_zero_previous_spending():
    expenses = [
        {
            "id": 1,
            "date": "2026-11-01",
            "category": "Food",
            "amount": "1000",
            "note": "Lunch"
        }
    ]

    result = compare_monthly_spending(
        "2026-11",
        expenses
    )

    food = result["categories"]["Food"]

    assert food["previous_spending"] == 0
    assert food["current_spending"] == 1000
    assert food["percentage_change"] is None


def test_invalid_month():
    with pytest.raises(ValueError):
        generate_monthly_summary(
            "2026-13",
            [],
            []
        )
