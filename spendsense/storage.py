import json
import os
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# JSON database files
EXPENSE_FILE = DATA_DIR / "expenses.json"
BUDGET_FILE = DATA_DIR / "budgets.json"


def load_data(file_path):
    """Load records from a JSON file."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                f"Invalid structure in {file_path.name}. "
                "Expected a JSON list."
            )

        return data

    except json.JSONDecodeError as error:
        raise ValueError(
            f"{file_path.name} contains invalid JSON. "
            "Repair the file before continuing."
        ) from error


def save_data(file_path, data):
    """Save records using a temporary file and atomic replacement."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temporary_file = file_path.with_name(
        file_path.name + ".tmp"
    )

    try:
        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temporary_file, file_path)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()


def load_expenses():
    return load_data(EXPENSE_FILE)


def save_expenses(expenses):
    save_data(EXPENSE_FILE, expenses)


def load_budgets():
    return load_data(BUDGET_FILE)


def save_budgets(budgets):
    save_data(BUDGET_FILE, budgets)