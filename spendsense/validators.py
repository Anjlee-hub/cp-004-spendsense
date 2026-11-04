from datetime import datetime
from decimal import Decimal, InvalidOperation


def validate_date(date_string):
    """Validate a date in YYYY-MM-DD format."""

    if not isinstance(date_string, str):
        raise ValueError("Date must be text in YYYY-MM-DD format.")

    try:
        parsed_date = datetime.strptime(date_string, "%Y-%m-%d")

        # Reject dates that are not in the exact expected format.
        if parsed_date.strftime("%Y-%m-%d") != date_string:
            raise ValueError

        return date_string

    except ValueError:
        raise ValueError("Invalid date. Use YYYY-MM-DD format.")


def validate_amount(amount):
    """Validate and normalize an expense amount."""

    try:
        value = Decimal(str(amount).strip())

        if not value.is_finite():
            raise ValueError("Amount must be a valid finite number.")

        if value <= 0:
            raise ValueError("Amount must be greater than zero.")

        if value.as_tuple().exponent < -2:
            raise ValueError("Amount cannot have more than 2 decimal places.")

        return value.quantize(Decimal("0.01"))

    except (InvalidOperation, AttributeError):
        raise ValueError("Enter a valid numeric amount.")


def validate_category(category):
    """Validate and normalize an expense category."""

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    return category.strip().title()


def validate_note(note):
    """Validate an optional expense note."""

    if note is None:
        return ""

    if not isinstance(note, str):
        raise ValueError("Note must be text.")

    return note.strip()


def validate_month(month):
    """Validate a month in YYYY-MM format."""

    if not isinstance(month, str):
        raise ValueError("Month must be in YYYY-MM format.")

    try:
        parsed_month = datetime.strptime(month, "%Y-%m")

        if parsed_month.strftime("%Y-%m") != month:
            raise ValueError

        return month

    except ValueError:
        raise ValueError("Invalid month. Use YYYY-MM format.")