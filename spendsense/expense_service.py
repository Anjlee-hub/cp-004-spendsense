from spendsense.storage import load_expenses, save_expenses

from spendsense.validators import (
    validate_date,
    validate_amount,
    validate_category,
    validate_note,
    validate_month
)


def get_next_id(expenses):
    """Generate the next unique expense ID."""

    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1


def add_expense(date, category, amount, note=""):
    """Add a new expense and save it to JSON."""

    date = validate_date(date)
    category = validate_category(category)
    amount = validate_amount(amount)
    note = validate_note(note)

    expenses = load_expenses()

    expense = {
        "id": get_next_id(expenses),
        "date": date,
        "category": category,
        "amount": str(amount),
        "note": note
    }

    expenses.append(expense)

    save_expenses(expenses)

    return expense


def view_expenses():
    """Return all stored expenses, ordered by ID."""

    expenses = load_expenses()

    return sorted(expenses, key=lambda expense: expense["id"])


def edit_expense(
    expense_id,
    date=None,
    category=None,
    amount=None,
    note=None
):
    """Edit an existing expense using its ID."""

    expenses = load_expenses()

    for expense in expenses:

        if expense["id"] == expense_id:

            if date is not None:
                expense["date"] = validate_date(date)

            if category is not None:
                expense["category"] = validate_category(category)

            if amount is not None:
                expense["amount"] = str(validate_amount(amount))

            if note is not None:
                expense["note"] = validate_note(note)

            save_expenses(expenses)

            return expense

    raise ValueError("Expense ID not found.")


def delete_expense(expense_id):
    """Delete an expense using its ID."""

    expenses = load_expenses()

    updated_expenses = [
        expense for expense in expenses
        if expense["id"] != expense_id
    ]

    if len(updated_expenses) == len(expenses):
        raise ValueError("Expense ID not found.")

    save_expenses(updated_expenses)

    return True


def get_expenses_by_month(month):
    """Return expenses belonging to a particular month."""

    month = validate_month(month)

    expenses = load_expenses()

    monthly_expenses = [
        expense for expense in expenses
        if expense["date"].startswith(month)
    ]

    return sorted(
        monthly_expenses,
        key=lambda expense: (expense["date"], expense["id"])
    )