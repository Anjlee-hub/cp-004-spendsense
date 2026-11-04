import csv
from pathlib import Path

from spendsense.expense_service import get_expenses_by_month
from spendsense.validators import validate_month


BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "exports"


def export_monthly_expenses(month):
    """Export a month's expenses into a CSV file."""

    month = validate_month(month)

    expenses = get_expenses_by_month(month)

    if not expenses:
        raise ValueError("No expenses found for this month.")

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = EXPORT_DIR / f"expenses_{month}.csv"

    fieldnames = [
        "id",
        "date",
        "category",
        "amount",
        "note"
    ]

    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(expenses)

    return file_path