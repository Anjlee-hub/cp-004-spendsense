
from decimal import Decimal, InvalidOperation
from datetime import datetime


def to_decimal(value):
    """Convert a monetary value to Decimal."""
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")

    if not result.is_finite():
        raise ValueError("Amount must be finite.")

    return result.quantize(Decimal("0.01"))


def validate_month(month):
    """Validate YYYY-MM month format."""
    try:
        datetime.strptime(month, "%Y-%m")

        if len(month) != 7:
            raise ValueError

        return month

    except (ValueError, TypeError):
        raise ValueError("Month must be in YYYY-MM format.")


def normalize_category(category):
    """Normalize category for consistent comparison."""
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    return category.strip().casefold()


def get_previous_month(month):
    """Return the previous month in YYYY-MM format."""
    validate_month(month)

    year, month_number = map(int, month.split("-"))

    if month_number == 1:
        year -= 1
        month_number = 12
    else:
        month_number -= 1

    return f"{year:04d}-{month_number:02d}"


def filter_expenses_by_month(expenses, month):
    """Filter expenses by their actual expense date."""
    validate_month(month)

    result = []

    for expense in expenses:
        expense_date = expense.get("date", "")

        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid expense date: {expense_date}"
            )

        if expense_date[:7] == month:
            result.append(expense)

    return result


def generate_monthly_summary(month, expenses, budgets):
    """
    Generate category-wise monthly spending summary.

    expenses: list of expense dictionaries
    budgets: list of budget dictionaries
    """
    validate_month(month)

    monthly_expenses = filter_expenses_by_month(expenses, month)

    category_spending = {}
    category_names = {}

    for expense in monthly_expenses:
        category = expense["category"]
        normalized = normalize_category(category)

        amount = to_decimal(expense["amount"])

        category_spending[normalized] = (
            category_spending.get(normalized, Decimal("0.00"))
            + amount
        )

        category_names.setdefault(normalized, category.strip())

    category_budgets = {}

    for budget in budgets:
        if budget["month"] != month:
            continue

        normalized = normalize_category(budget["category"])

        category_budgets[normalized] = to_decimal(budget["amount"])
        category_names.setdefault(
            normalized,
            budget["category"].strip()
        )

    all_categories = set(category_spending) | set(category_budgets)

    category_summary = {}

    total_spent = Decimal("0.00")
    total_budget = Decimal("0.00")

    for category in sorted(all_categories):
        spent = category_spending.get(
            category,
            Decimal("0.00")
        )

        budget = category_budgets.get(
            category,
            Decimal("0.00")
        )

        remaining = budget - spent

        utilization = (
            (spent / budget) * Decimal("100")
            if budget > 0
            else None
        )

        category_summary[category_names[category]] = {
            "spent": spent,
            "budget": budget,
            "remaining": remaining,
            "utilization": utilization,
            "exceeded": spent > budget if budget > 0 else False
        }

        total_spent += spent
        total_budget += budget

    total_remaining = total_budget - total_spent

    overall_utilization = (
        (total_spent / total_budget) * Decimal("100")
        if total_budget > 0
        else None
    )

    return {
        "month": month,
        "total_spent": total_spent,
        "total_budget": total_budget,
        "remaining": total_remaining,
        "utilization": overall_utilization,
        "categories": category_summary
    }


def get_top_five_expenses(month, expenses):
    """Return the five largest expenses for a selected month."""
    monthly_expenses = filter_expenses_by_month(expenses, month)

    sorted_expenses = sorted(
        monthly_expenses,
        key=lambda expense: (
            -to_decimal(expense["amount"]),
            expense["date"],
            str(expense.get("id", ""))
        )
    )

    return sorted_expenses[:5]


def compare_monthly_spending(current_month, expenses):
    """
    Compare spending between current and previous month.

    Percentage change is None if previous spending is zero.
    """
    validate_month(current_month)

    previous_month = get_previous_month(current_month)

    current_expenses = filter_expenses_by_month(
        expenses,
        current_month
    )

    previous_expenses = filter_expenses_by_month(
        expenses,
        previous_month
    )

    current_totals = {}
    previous_totals = {}
    category_names = {}

    for expense in current_expenses:
        category = expense["category"]
        normalized = normalize_category(category)

        current_totals[normalized] = (
            current_totals.get(normalized, Decimal("0.00"))
            + to_decimal(expense["amount"])
        )

        category_names.setdefault(normalized, category.strip())

    for expense in previous_expenses:
        category = expense["category"]
        normalized = normalize_category(category)

        previous_totals[normalized] = (
            previous_totals.get(normalized, Decimal("0.00"))
            + to_decimal(expense["amount"])
        )

        category_names.setdefault(normalized, category.strip())

    all_categories = set(current_totals) | set(previous_totals)

    comparison = {}

    for category in sorted(all_categories):
        current = current_totals.get(
            category,
            Decimal("0.00")
        )

        previous = previous_totals.get(
            category,
            Decimal("0.00")
        )

        change = current - previous

        percentage_change = (
            (change / previous) * Decimal("100")
            if previous != 0
            else None
        )

        comparison[category_names[category]] = {
            "previous_month": previous_month,
            "current_month": current_month,
            "previous_spending": previous,
            "current_spending": current,
            "change": change,
            "percentage_change": percentage_change
        }

    return {
        "previous_month": previous_month,
        "current_month": current_month,
        "categories": comparison
    }
