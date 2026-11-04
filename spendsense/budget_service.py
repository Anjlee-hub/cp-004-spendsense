
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import datetime


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "budgets.json"


def validate_month(month):
    """Validate month format YYYY-MM."""
    try:
        datetime.strptime(month, "%Y-%m")
        if len(month) != 7:
            raise ValueError
        return month
    except (ValueError, TypeError):
        raise ValueError("Month must be in YYYY-MM format.")


def normalize_category(category):
    """Normalize category for consistent matching."""
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    return category.strip().casefold()


def validate_amount(amount):
    """Convert amount to Decimal and validate it."""
    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Budget amount must be a valid number.")

    if not amount.is_finite() or amount <= 0:
        raise ValueError("Budget amount must be greater than zero.")

    return amount.quantize(Decimal("0.01"))


def load_budgets():
    """Load budgets from JSON storage."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("budgets.json contains invalid JSON.")

    if not isinstance(data, list):
        raise ValueError("Budget data must be a JSON list.")

    return data


def save_budgets(budgets):
    """Save budgets to JSON storage."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(budgets, file, indent=4)


def get_budgets(month):
    """Return all budgets for a selected month."""
    validate_month(month)

    budgets = load_budgets()

    return [
        budget for budget in budgets
        if budget["month"] == month
    ]


def get_budget(month, category):
    """Return the budget for a specific category and month."""
    validate_month(month)
    normalized = normalize_category(category)

    for budget in load_budgets():
        if (
            budget["month"] == month
            and normalize_category(budget["category"]) == normalized
        ):
            return Decimal(str(budget["amount"]))

    return None


def set_budget(month, category, amount):
    """Set a new budget or update an existing one."""
    validate_month(month)
    normalized = normalize_category(category)
    amount = validate_amount(amount)

    budgets = load_budgets()

    for budget in budgets:
        if (
            budget["month"] == month
            and normalize_category(budget["category"]) == normalized
        ):
            budget["amount"] = str(amount)
            save_budgets(budgets)
            return budget

    new_budget = {
        "month": month,
        "category": category.strip(),
        "amount": str(amount)
    }

    budgets.append(new_budget)
    save_budgets(budgets)

    return new_budget


def update_budget(month, category, amount):
    """Update an existing budget."""
    existing_budget = get_budget(month, category)

    if existing_budget is None:
        raise ValueError("Budget does not exist for this category and month.")

    return set_budget(month, category, amount)


def delete_budget(month, category):
    """Delete a budget for a category and month."""
    validate_month(month)
    normalized = normalize_category(category)

    budgets = load_budgets()

    updated_budgets = [
        budget for budget in budgets
        if not (
            budget["month"] == month
            and normalize_category(budget["category"]) == normalized
        )
    ]

    if len(updated_budgets) == len(budgets):
        return False

    save_budgets(updated_budgets)
    return True
