from decimal import Decimal, InvalidOperation

from spendsense.expense_service import (
    add_expense,
    view_expenses,
    edit_expense,
    delete_expense,
)

from spendsense.budget_service import (
    get_budgets,
    get_budget,
    set_budget,
    delete_budget,
    load_budgets,
)

from spendsense.alert_service import (
    calculate_utilization,
    check_budget_thresholds,
)

from spendsense.report_service import (
    generate_monthly_summary,
    get_top_five_expenses,
    compare_monthly_spending,
)

from spendsense.csv_export import export_monthly_expenses


# --------------------------------------------------
# GENERAL DISPLAY HELPERS
# --------------------------------------------------

def format_money(amount):
    """Format a monetary value to two decimal places."""
    return f"INR {Decimal(str(amount)):,.2f}"


def get_category_spending(expenses, month, category):
    """Calculate total spending for a category in a month."""

    total = Decimal("0.00")

    for expense in expenses:
        if (
            expense["date"].startswith(month)
            and expense["category"].strip().casefold()
            == category.strip().casefold()
        ):
            total += Decimal(str(expense["amount"]))

    return total


def display_expenses(expenses):
    """Display expenses in a formatted table."""

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n" + "=" * 95)
    print(
        f"{'ID':<6}"
        f"{'DATE':<15}"
        f"{'CATEGORY':<20}"
        f"{'AMOUNT':<20}"
        f"NOTE"
    )
    print("=" * 95)

    for expense in expenses:
        print(
            f"{expense['id']:<6}"
            f"{expense['date']:<15}"
            f"{expense['category']:<20}"
            f"{format_money(expense['amount']):<20}"
            f"{expense['note']}"
        )

    print("=" * 95)


def display_alerts(alerts):
    """Display budget threshold alerts."""

    if not alerts:
        return

    print("\n" + "!" * 55)
    print("             BUDGET ALERT")
    print("!" * 55)

    for alert in alerts:
        print(alert["message"])

    print("!" * 55)


def check_expense_alert(month, category, previous_spending,
                        updated_spending):
    """
    Check whether an expense change crosses a budget threshold.

    Alerts are generated only when spending increases and crosses
    the configured 80% or 100% budget threshold.
    """

    if updated_spending <= previous_spending:
        return

    budget = get_budget(month, category)

    if budget is None or budget <= 0:
        return

    alerts = check_budget_thresholds(
        month=month,
        category=category,
        previous_spending=previous_spending,
        updated_spending=updated_spending,
        budget=budget,
    )

    display_alerts(alerts)


# --------------------------------------------------
# EXPENSE MANAGEMENT
# --------------------------------------------------

def add_expense_menu():
    """Collect details and add a new expense."""

    print("\n--- ADD EXPENSE ---")

    date = input("Enter date (YYYY-MM-DD): ").strip()
    category = input("Enter category: ").strip()
    amount = input("Enter amount: ").strip()
    note = input("Enter note (optional): ").strip()

    month = date[:7]

    previous_expenses = view_expenses()
    previous_spending = get_category_spending(
        previous_expenses, month, category
    )

    expense = add_expense(date, category, amount, note)

    print("\nExpense added successfully!")
    print("Expense ID:", expense["id"])
    print("Amount:", format_money(expense["amount"]))

    updated_expenses = view_expenses()
    updated_spending = get_category_spending(
        updated_expenses, month, category
    )

    check_expense_alert(
        month,
        category,
        previous_spending,
        updated_spending,
    )


def view_expenses_menu():
    """Display all stored expenses."""

    print("\n--- ALL EXPENSES ---")

    expenses = view_expenses()
    display_expenses(expenses)


def edit_expense_menu():
    """Edit an existing expense."""

    print("\n--- EDIT EXPENSE ---")

    expense_id = int(input("Enter Expense ID: "))

    expenses_before = view_expenses()

    old_expense = next(
        (
            expense for expense in expenses_before
            if expense["id"] == expense_id
        ),
        None,
    )

    if old_expense is None:
        raise ValueError("Expense ID not found.")

    old_month = old_expense["date"][:7]
    old_category = old_expense["category"]

    print("\nCurrent expense:")
    display_expenses([old_expense])

    print("\nLeave a field empty to keep its current value.")

    date = input("New date (YYYY-MM-DD): ").strip() or None
    category = input("New category: ").strip() or None
    amount = input("New amount: ").strip() or None
    note = input("New note: ").strip() or None

    # Capture spending in the destination category/month
    # before modifying the expense.
    new_month = (date or old_expense["date"])[:7]
    new_category = category or old_expense["category"]

    previous_new_group_spending = get_category_spending(
        expenses_before,
        new_month,
        new_category,
    )

    updated_expense = edit_expense(
        expense_id,
        date=date,
        category=category,
        amount=amount,
        note=note,
    )

    print("\nExpense updated successfully!")
    print(updated_expense)

    expenses_after = view_expenses()

    updated_new_group_spending = get_category_spending(
        expenses_after,
        new_month,
        new_category,
    )

    check_expense_alert(
        new_month,
        new_category,
        previous_new_group_spending,
        updated_new_group_spending,
    )


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


# --------------------------------------------------
# BUDGET MANAGEMENT
# --------------------------------------------------

def set_budget_menu():
    """Set or update a monthly category budget."""

    print("\n--- SET MONTHLY BUDGET ---")

    month = input("Enter month (YYYY-MM): ").strip()
    category = input("Enter category: ").strip()
    amount = input("Enter budget amount: ").strip()

    budget = set_budget(month, category, amount)

    print("\nBudget saved successfully!")
    print("Month:", budget["month"])
    print("Category:", budget["category"])
    print("Budget:", format_money(budget["amount"]))


def view_budgets_menu():
    """Display budgets for a selected month."""

    print("\n--- VIEW MONTHLY BUDGETS ---")

    month = input("Enter month (YYYY-MM): ").strip()

    budgets = get_budgets(month)

    if not budgets:
        print("\nNo budgets found for", month)
        return

    print("\nBudgets for", month)
    print("-" * 60)
    print(f"{'CATEGORY':<25}{'BUDGET':>25}")
    print("-" * 60)

    for budget in budgets:
        print(
            f"{budget['category']:<25}"
            f"{format_money(budget['amount']):>25}"
        )

    print("-" * 60)


def view_budget_status_menu():
    """Display current spending against monthly budgets."""

    print("\n--- MONTHLY BUDGET STATUS ---")

    month = input("Enter month (YYYY-MM): ").strip()

    expenses = view_expenses()
    budgets = load_budgets()

    summary = generate_monthly_summary(
        month,
        expenses,
        budgets,
    )

    if not summary["categories"]:
        print("\nNo expenses or budgets found for", month)
        return

    print("\nBudget status for", month)
    print("=" * 95)

    print(
        f"{'CATEGORY':<20}"
        f"{'SPENT':>18}"
        f"{'BUDGET':>18}"
        f"{'REMAINING':>18}"
        f"{'USED':>12}"
    )

    print("=" * 95)

    for category, details in summary["categories"].items():

        utilization = details["utilization"]

        if utilization is None:
            used = "N/A"
        else:
            used = f"{utilization:.2f}%"

        print(
            f"{category:<20}"
            f"{format_money(details['spent']):>18}"
            f"{format_money(details['budget']):>18}"
            f"{format_money(details['remaining']):>18}"
            f"{used:>12}"
        )

        if details["exceeded"]:
            print("  WARNING: Budget exceeded!")

    print("=" * 95)

    print("Total spent:", format_money(summary["total_spent"]))
    print("Total budget:", format_money(summary["total_budget"]))
    print("Remaining:", format_money(summary["remaining"]))

    if summary["utilization"] is not None:
        print(
            "Overall utilization:",
            f"{summary['utilization']:.2f}%"
        )


# --------------------------------------------------
# REPORTS AND ANALYTICS
# --------------------------------------------------

def monthly_summary_menu():
    """Generate a monthly spending summary."""

    print("\n--- MONTHLY SUMMARY ---")

    month = input("Enter month (YYYY-MM): ").strip()

    expenses = view_expenses()
    budgets = load_budgets()

    summary = generate_monthly_summary(
        month,
        expenses,
        budgets,
    )

    print("\nMonthly Summary:", summary["month"])
    print("-" * 60)

    print("Total spent:", format_money(summary["total_spent"]))
    print("Total budget:", format_money(summary["total_budget"]))
    print("Remaining:", format_money(summary["remaining"]))

    if summary["utilization"] is not None:
        print(
            "Budget utilization:",
            f"{summary['utilization']:.2f}%"
        )
    else:
        print("Budget utilization: Not available")

    print("\nCategory-wise Summary")
    print("-" * 85)

    for category, details in summary["categories"].items():

        print("\nCategory:", category)
        print("Spent:", format_money(details["spent"]))
        print("Budget:", format_money(details["budget"]))
        print("Remaining:", format_money(details["remaining"]))

        if details["utilization"] is not None:
            print(
                "Utilization:",
                f"{details['utilization']:.2f}%"
            )
        else:
            print("Utilization: No budget set")

        if details["exceeded"]:
            print("Status: OVER BUDGET")
        else:
            print("Status: Within budget")


def top_five_menu():
    """Display the five largest expenses for a month."""

    print("\n--- TOP 5 LARGEST EXPENSES ---")

    month = input("Enter month (YYYY-MM): ").strip()

    expenses = view_expenses()

    top_expenses = get_top_five_expenses(
        month,
        expenses,
    )

    if not top_expenses:
        print("\nNo expenses found for", month)
        return

    print("\nTop expenses for", month)
    display_expenses(top_expenses)


def compare_months_menu():
    """Compare spending in the selected month with the previous month."""

    print("\n--- MONTHLY SPENDING COMPARISON ---")

    month = input("Enter current month (YYYY-MM): ").strip()

    expenses = view_expenses()

    comparison = compare_monthly_spending(
        month,
        expenses,
    )

    print(
        "\nComparing",
        comparison["current_month"],
        "with",
        comparison["previous_month"],
    )

    print("-" * 90)

    if not comparison["categories"]:
        print("No expenses found in either month.")
        return

    for category, details in comparison["categories"].items():

        print("\nCategory:", category)

        print(
            "Previous month:",
            format_money(details["previous_spending"]),
        )

        print(
            "Current month:",
            format_money(details["current_spending"]),
        )

        print(
            "Change:",
            format_money(details["change"]),
        )

        percentage = details["percentage_change"]

        if percentage is None:
            print("Percentage change: Not available (no previous spending)")
        else:
            print(
                "Percentage change:",
                f"{percentage:.2f}%"
            )

        if details["change"] > 0:
            print("Trend: Spending increased")
        elif details["change"] < 0:
            print("Trend: Spending decreased")
        else:
            print("Trend: No change")


# --------------------------------------------------
# CSV EXPORT
# --------------------------------------------------

def export_expenses_menu():
    """Export monthly expenses to CSV."""

    print("\n--- EXPORT MONTHLY EXPENSES ---")

    month = input("Enter month (YYYY-MM): ").strip()

    file_path = export_monthly_expenses(month)

    print("\nCSV exported successfully!")
    print("Saved at:", file_path)


# --------------------------------------------------
# MAIN MENU
# --------------------------------------------------

def main():
    """Run the SpendSense Smart Budget Monitoring System."""

    while True:

        print("\n")
        print("=" * 50)
        print("                 SPENDSENSE")
        print("          SMART BUDGET MONITORING")
        print("=" * 50)

        print("1.  Add Expense")
        print("2.  View All Expenses")
        print("3.  Edit Expense")
        print("4.  Delete Expense")
        print("5.  Set Monthly Budget")
        print("6.  View Monthly Budgets")
        print("7.  View Budget Status")
        print("8.  Generate Monthly Summary")
        print("9.  Show Top 5 Expenses")
        print("10. Compare Monthly Spending")
        print("11. Export Monthly Expenses to CSV")
        print("12. Exit")

        print("=" * 50)

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
                set_budget_menu()

            elif choice == "6":
                view_budgets_menu()

            elif choice == "7":
                view_budget_status_menu()

            elif choice == "8":
                monthly_summary_menu()

            elif choice == "9":
                top_five_menu()

            elif choice == "10":
                compare_months_menu()

            elif choice == "11":
                export_expenses_menu()

            elif choice == "12":
                print("\nThank you for using SpendSense!")
                break

            else:
                print("\nInvalid choice. Select a number from 1 to 12.")

        except ValueError as error:
            print("\nInput error:", error)

        except OSError as error:
            print("\nFile operation error:", error)

        except InvalidOperation:
            print("\nInput error: Invalid monetary value.")

        except KeyboardInterrupt:
            print("\n\nApplication interrupted.")
            break


if __name__ == "__main__":
    main()