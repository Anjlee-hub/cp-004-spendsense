from decimal import Decimal

from spendsense.expense_service import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense
)

from spendsense.csv_export import export_monthly_expenses


def display_expenses(expenses):
    """Display expenses in a formatted table."""

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 85)
    print(
        f"{'ID':<6}"
        f"{'DATE':<15}"
        f"{'CATEGORY':<18}"
        f"{'AMOUNT':<15}"
        f"{'NOTE'}"
    )
    print("=" * 85)

    for expense in expenses:
        print(
            f"{expense['id']:<6}"
            f"{expense['date']:<15}"
            f"{expense['category']:<18}"
            f"₹{expense['amount']:<14}"
            f"{expense['note']}"
        )

    print("=" * 85)


def add_expense_menu():
    """Collect input and add an expense."""

    print("\n--- ADD EXPENSE ---")

    date = input("Enter date (YYYY-MM-DD): ").strip()
    category = input("Enter category: ").strip()
    amount = input("Enter amount: ").strip()
    note = input("Enter note (optional): ").strip()

    expense = add_expense(date, category, amount, note)

    print("\nExpense added successfully!")
    print("Expense ID:", expense["id"])


def view_expenses_menu():
    """Display all stored expenses."""

    print("\n--- ALL EXPENSES ---")

    expenses = view_expenses()

    display_expenses(expenses)


def edit_expense_menu():
    """Collect updated details for an expense."""

    print("\n--- EDIT EXPENSE ---")

    expense_id = int(input("Enter Expense ID: "))

    print("Leave a field empty to keep its current value.")

    date = input("New date (YYYY-MM-DD): ").strip() or None

    category = input("New category: ").strip() or None

    amount = input("New amount: ").strip() or None

    note = input("New note: ").strip()

    if note == "":
        note = None

    updated_expense = edit_expense(
        expense_id,
        date=date,
        category=category,
        amount=amount,
        note=note
    )

    print("\nExpense updated successfully!")
    print(updated_expense)


def delete_expense_menu():
    """Delete an expense after confirmation."""

    print("\n--- DELETE EXPENSE ---")

    expense_id = int(input("Enter Expense ID: "))

    confirmation = input(
        "Confirm deletion? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        delete_expense(expense_id)

        print("\nExpense deleted successfully!")

    else:
        print("\nDeletion cancelled.")


def export_expenses_menu():
    """Export a selected month's expenses."""

    print("\n--- EXPORT MONTHLY EXPENSES ---")

    month = input("Enter month (YYYY-MM): ").strip()

    file_path = export_monthly_expenses(month)

    print("\nCSV exported successfully!")
    print("Saved at:", file_path)


def main():
    """Run the SpendSense expense management menu."""

    while True:

        print("\n")
        print("=" * 40)
        print("          SPENDSENSE")
        print("     SMART BUDGET MONITORING")
        print("=" * 40)

        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Export Monthly Expenses to CSV")
        print("6. Exit")

        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        try:

            if choice == "1":
                add_expense_menu()

            elif choice == "2":
                view_expenses_menu()

            elif choice == "3":
                edit_expense_menu()

            elif choice == "4":
                delete_expense_menu()

            elif choice == "5":
                export_expenses_menu()

            elif choice == "6":
                print("\nThank you for using SpendSense!")
                break

            else:
                print("\nInvalid choice. Select 1 to 6.")

        except ValueError as error:
            print("\nInput error:", error)

        except OSError as error:
            print("\nFile operation error:", error)


if __name__ == "__main__":
    main()