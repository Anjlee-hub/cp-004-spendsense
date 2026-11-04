# SpendSense – Smart Budget Monitoring System

**Capstone ID:** CP-002  
**Domain:** Banking and FinTech  
**Project Type:** Group Project  
**Team Size:** 2 Members  
**Project Level:** Foundation

---

## 1. Project Overview

SpendSense is a Python-based personal finance management application designed to help students and young professionals record expenses, manage monthly budgets, monitor spending patterns, and avoid overspending.

The application provides a menu-driven command-line interface (CLI) through which users can manage expenses, configure category-wise monthly budgets, receive threshold alerts, generate financial summaries, compare monthly spending, and export expense records.

SpendSense uses JSON files for persistent data storage and Python modules for expense management, budget calculations, alerts, and reporting.

## 2. Problem Statement

Students and young professionals often exceed their monthly budgets because they lack a simple and structured way to record expenses and monitor category-wise spending.

SpendSense addresses this problem by providing an accessible system for recording transactions, setting monthly spending limits, tracking budget utilization, and generating timely alerts when spending reaches critical thresholds.

## 3. Project Objectives

- Simplify daily expense tracking.
- Enable monthly budget allocation by expense category.
- Generate alerts when spending reaches 80% and 100% of a budget.
- Provide monthly spending summaries.
- Identify the five largest expenses in a selected month.
- Compare spending between consecutive months.
- Export monthly expense records into CSV format.
- Improve financial awareness through structured spending reports.

## 4. Features and Functionality

### 4.1 Expense Management
- Add expenses with date, category, amount, and note.
- View all recorded expenses.
- Edit existing expense records.
- Delete expense records.
- Filter expenses by month.
- Persist expense records using JSON storage.

### 4.2 Monthly Category Budgets
- Set monthly budgets for individual categories.
- View configured budgets.
- Update existing budget allocations.
- Delete budget records through the budget service.
- Calculate spending against allocated budgets.

### 4.3 Budget Threshold Alerts
- **80% alert:** Notify the user when spending crosses 80% of the category budget.
- **100% alert:** Notify the user when spending reaches or exceeds the full budget.
- Detect transactions that cross both thresholds.
- Avoid duplicate alerts when a threshold has already been crossed.
- Handle zero-budget cases safely.

### 4.4 Monthly Budget Status
Display:
- Category-wise spending.
- Allocated budget.
- Remaining budget.
- Budget utilization percentage.
- Budget-exceeded status.
- Overall monthly spending and budget totals.

### 4.5 Monthly Summary
Generate a monthly report containing:
- Total expenditure.
- Total allocated budget.
- Remaining budget.
- Overall budget utilization.
- Category-wise financial summaries.

### 4.6 Top 5 Largest Expenses
- Identify the five largest expenses for a selected month.
- Sort expenses in descending order of amount.
- Display transaction ID, date, category, amount, and note.

### 4.7 Month-over-Month Comparison
- Compare the selected month with the previous month.
- Calculate category-wise spending differences.
- Display percentage changes when previous-month spending is nonzero.
- Identify increasing and decreasing spending trends.

### 4.8 CSV Export
- Export monthly expense records into CSV files.
- Include transaction ID, date, category, amount, and note.
- Generate month-specific export files.

## 5. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Application Interface | Command-Line Interface (CLI) |
| Data Storage | JSON |
| Data Export | CSV |
| Testing Framework | Pytest |
| Version Control | Git |
| Repository Hosting | GitHub |
| Development Environment | Visual Studio Code |

## 6. System Architecture

SpendSense follows a modular, service-oriented Python architecture.

```text
                 +-----------------------+
                 |         User          |
                 +-----------+-----------+
                             |
                             v
                 +-----------------------+
                 |      main.py          |
                 |   CLI / Menu System   |
                 +-----------+-----------+
                             |
             +---------------+----------------+
             |               |                |
             v               v                v
     +---------------+ +-------------+ +---------------+
     | Expense       | | Budget      | | Report        |
     | Service       | | Service     | | Service       |
     +-------+-------+ +------+------+ +-------+-------+
             |                |                |
             |                v                |
             |        +---------------+        |
             |        | Alert Service |        |
             |        +---------------+        |
             |                |                |
             +----------------+----------------+
                              |
                              v
                    +-------------------+
                    |  Storage Module   |
                    +---------+---------+
                              |
                   +----------+----------+
                   |                     |
                   v                     v
             +-----------+         +-----------+
             | expenses  |         | budgets   |
             | .json     |         | .json     |
             +-----------+         +-----------+

                    CSV Export Module
                              |
                              v
                    +-------------------+
                    | Monthly CSV Files |
                    +-------------------+
```

### Architecture Components

- **main.py:** Handles the interactive menu and coordinates application services.
- **expense_service.py:** Implements expense creation, viewing, editing, and deletion.
- **budget_service.py:** Manages monthly category budgets.
- **alert_service.py:** Calculates budget utilization and detects threshold crossings.
- **report_service.py:** Generates monthly summaries, top-five expense reports, and monthly comparisons.
- **storage.py:** Handles persistent JSON data operations.
- **csv_export.py:** Exports monthly expense records.
- **validators.py:** Handles input validation.

## 7. Project Structure

```text
CP_2_spendsense/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── expenses.json
│   └── budgets.json
│
├── spendsense/
│   ├── __init__.py
│   ├── expense_service.py
│   ├── budget_service.py
│   ├── alert_service.py
│   ├── report_service.py
│   ├── storage.py
│   ├── csv_export.py
│   └── validators.py
│
├── exports/
│
└── tests/
    ├── __init__.py
    ├── test_alerts.py
    ├── test_budgets.py
    ├── test_csv_export.py
    ├── test_expenses.py
    └── test_reports.py
```

## 8. Installation and Setup

### Prerequisites

- Python 3.10 or later (Python 3.13.2 was used during project verification).
- Git.
- Visual Studio Code or another Python-compatible editor.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Anjlee-hub/cp-004-spendsense.git
cd cp-004-spendsense
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Run the Application

From the project root directory:

```bash
python main.py
```

The SpendSense main menu will appear in the terminal.

## 9. Application Menu

The application provides the following 12 options:

| Option | Function |
|---|---|
| 1 | Add Expense |
| 2 | View All Expenses |
| 3 | Edit Expense |
| 4 | Delete Expense |
| 5 | Set Monthly Budget |
| 6 | View Monthly Budgets |
| 7 | View Budget Status |
| 8 | Generate Monthly Summary |
| 9 | Show Top 5 Expenses |
| 10 | Compare Monthly Spending |
| 11 | Export Monthly Expenses to CSV |
| 12 | Exit |

## 10. Budget Calculation

### Budget Utilization

Budget Utilization (%) = (Total Category Spending / Monthly Category Budget) × 100

### Remaining Budget

Remaining Budget = Monthly Category Budget − Total Category Spending

### Illustrative Example

| Category | Monthly Budget | Amount Spent | Utilization | Status |
|---|---:|---:|---:|---|
| Food | ₹3,000 | ₹1,500 | 50% | Within budget |
| Transport | ₹2,000 | ₹1,700 | 85% | 80% threshold crossed |
| Shopping | ₹2,500 | ₹2,600 | 104% | Budget exceeded |

*These figures are illustrative examples.*

## 11. Testing

SpendSense uses Pytest for automated unit testing.

Run the test suite from the project root:

```bash
python -m pytest -v
```

### Test Coverage

| Test Module | Main Functionality |
|---|---|
| test_expenses.py | Expense creation, viewing, editing, deletion, validation, and filtering |
| test_budgets.py | Budget creation, updating, retrieval, deletion, validation, and persistence |
| test_alerts.py | Threshold detection, utilization, and edge cases |
| test_reports.py | Monthly summaries, top-five reports, and month comparisons |
| test_csv_export.py | CSV generation, empty-month handling, and validation |

### Latest Verification Results

- **Total automated tests:** 43
- **Passed:** 43
- **Failed:** 0
- **Execution time:** 0.58 seconds
- **Python version:** 3.13.2
- **Testing framework:** Pytest 9.2.0

All 43 automated tests passed during the final verification after the integration was merged into the GitHub main branch.

## 12. Version Control and Collaboration

The project is maintained using Git and GitHub.

Repository: https://github.com/Anjlee-hub/cp-004-spendsense

The team uses separate feature branches for development, pull requests for code review, and the main branch for integrated application code.

## 13. Future Enhancements

Potential future improvements include:

- Interactive spending charts and visual reports.
- User authentication and personalized financial dashboards.
- A graphical user interface.
- Database integration.
- Automated recurring expense tracking.
- Enhanced financial insights and spending recommendations.

## 14. Conclusion

SpendSense provides a modular and practical solution for personal expense tracking and monthly budget monitoring. It combines expense management, budget threshold alerts, financial reporting, month-over-month comparisons, and CSV export in a Python-based command-line application.

The project demonstrates modular programming, JSON-based persistence, input validation, financial calculations, automated testing, and collaborative software development using GitHub.

---

**Project:** SpendSense – Smart Budget Monitoring System
**Capstone ID:** CP-002
**Domain:** Banking and FinTech