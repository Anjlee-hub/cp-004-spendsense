# SpendSense — Smart Budget Monitoring System with Threshold Alerts

**Capstone ID:** CP-002  
**Domain:** Banking and FinTech  
**Project Type:** Group Project  
**Team Size:** 2 Members  
**Project Level:** Foundation

---

## 📌 Project Overview

**SpendSense** is a personal finance management application designed to help students and young professionals monitor their spending, manage monthly budgets, and avoid overspending.

Many people struggle to understand where their money goes before the end of the month. SpendSense addresses this problem by organizing expenses into categories, comparing actual expenditure against predefined budgets, and generating alerts when spending reaches critical thresholds.

The application provides a centralized dashboard for tracking expenses, reviewing monthly financial summaries, and identifying the five largest expenses in a selected month.

## 🎯 Problem Statement

Students and young professionals often exceed their monthly budgets because they lack a simple, structured way to record expenses and monitor category-wise spending.

SpendSense aims to provide an accessible solution that enables users to record transactions, set spending limits, receive timely budget alerts, and make informed financial decisions.

## 🎯 Project Objectives

- Simplify daily expense tracking.
- Enable monthly budget allocation by expense category.
- Alert users when spending reaches 80% and 100% of a category budget.
- Provide monthly spending summaries and budget comparisons.
- Identify the five largest expenses of the month.
- Encourage better financial awareness and spending habits.

## ✨ Core Features

The following five features are mandatory according to the CP-002 problem statement.

### 1. Expense Management
- Add an expense with its date, category, amount, and a short note.
- View recorded expenses.
- Organize transactions by category and month.

### 2. Monthly Category Budgets
- Set a monthly spending limit for each category.
- Track actual spending against allocated budgets.
- Calculate the remaining budget and percentage utilized.

### 3. Budget Threshold Alerts
- **80% alert:** Notify the user when category spending reaches 80% of its budget.
- **100% alert:** Notify the user when category spending reaches or exceeds its budget.
- Avoid repeatedly triggering the same threshold alert during routine dashboard refreshes.

### 4. Monthly Summary Dashboard
- Display total expenditure for the selected month.
- Compare spending against the budget for each category.
- Show budget utilization and remaining amounts.

### 5. Top 5 Largest Expenses
- Display the five highest-value expenses in the selected month.
- Sort transactions by amount in descending order.
- Show the date, category, amount, and note for each transaction.

## 🌟 Optional Enhancements

The following stretch features can be implemented after completing the mandatory requirements.

- Month-over-month spending comparison by category.
- Export monthly expense records to CSV.
- Interactive spending charts and visual reports.
- User authentication and personalized dashboards.
- Responsive design for mobile and desktop devices.

## 🛠️ Technology Stack

The proposed technology stack is listed below. Replace any technology that differs from the team's actual implementation.

| Component | Technology |
|---|---|
| Frontend | React.js |
| Frontend Tooling | Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Data Visualization | Recharts |
| API Documentation | FastAPI / Swagger UI |
| Testing | Pytest |
| Version Control | Git and GitHub |

## 🏗️ System Architecture

```text
                  +----------------------+
                  |         User         |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  |    React Frontend    |
                  +----------+-----------+
                             |
                       REST API Calls
                             |
                             v
                  +----------------------+
                  |    FastAPI Backend   |
                  +----------+-----------+
                             |
                +------------+------------+
                |                         |
                v                         v
       +----------------+       +----------------+
       | Expense Service|       |  Budget Service|
       +--------+-------+       +--------+-------+
                |                         |
                +------------+------------+
                             |
                             v
                  +----------------------+
                  | PostgreSQL Database  |
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | Budget Analysis and  |
                  | Threshold Alert Logic|
                  +----------+-----------+
                             |
                             v
                  +----------------------+
                  | Monthly Summary and  |
                  | Top 5 Expense Report |
                  +----------------------+
```

## 📊 Budget Calculation

### Budget Utilization

`Budget Utilization (%) = (Total Category Spending / Monthly Category Budget) × 100`

### Remaining Budget

`Remaining Budget = Monthly Category Budget − Total Category Spending`

### Example

| Category | Monthly Budget | Amount Spent | Utilization | Status |
|---|---:|---:|---:|---|
| Food | ₹3,000 | ₹1,500 | 50% | Within budget |
| Transport | ₹2,000 | ₹1,700 | 85% | 80% threshold crossed |
| Shopping | ₹2,500 | ₹2,600 | 104% | Budget exceeded |

*The figures above are illustrative examples, not actual application data.*

## 📁 Project Structure

The following is a suggested repository structure. Adapt it to the files and folders created by your team.

```text
CP_2_spendsense/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── screenshots/
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following tools before running the project:

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Anjlee-hub/cp-004-spendsense.git
cd cp-004-spendsense
```

### Step 2: Configure the Backend

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the database connection using environment variables or a local `.env` file. Create the PostgreSQL database and apply any required migrations before starting the server.

Run the backend:

```bash
uvicorn app.main:app --reload
```

API documentation, when the server is running:

`http://127.0.0.1:8000/docs`

### Step 3: Configure the Frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in the terminal.

> These commands assume the proposed folder structure. Adjust the paths and startup commands to match the actual project.

## 🧪 Testing

Run the backend tests from the backend directory:

```bash
pytest
```

Important test cases include:

- Adding and retrieving expenses.
- Calculating monthly totals by category.
- Triggering alerts at 80% and 100%.
- Handling an expense that crosses both thresholds in a single transaction.
- Displaying the five largest expenses in the correct order.
- Handling months with no expenses and categories without configured budgets.
- Validating expense amounts and dates.

## 🔐 Security and Data Integrity

- Validate all expense inputs on the backend.
- Use secure database access patterns and parameterized queries or an ORM.
- Keep database credentials and secret keys outside the source code.
- Do not commit `.env` files or real financial records.
- If multiple users are supported, enforce server-side authorization for every user-specific operation.
- Use decimal-safe arithmetic for monetary values.

## 👥 Team Members and Responsibilities

This project is developed collaboratively by a team of two members.

| Team Member | Responsibilities |
|---|---|
| **Member 1 — Anjlee S** | Frontend development, user interface, expense entry screens, dashboard integration, and UI testing |
| **Member 2 — [Member 2 Name]** | Backend development, database design, budget calculations, threshold alerts, and API testing |

**Collaboration:** Both members contribute to requirements analysis, integration, debugging, documentation, testing, and final project delivery.

*Update these responsibilities to reflect the work actually performed by each team member.*

## 🎓 Learning Outcomes

Through this project, the team gains practical experience in:

- Full-stack application development.
- REST API design and integration.
- Database modelling and CRUD operations.
- Category-wise aggregation and sorting algorithms.
- Date-based filtering and monthly calculations.
- Threshold-based alert logic.
- Software testing, Git, and collaborative development.

## 🔮 Future Scope

Potential future improvements include:

- Recurring expense tracking.
- Savings goals and progress monitoring.
- Automated expense categorization.
- Personalized spending insights using machine learning.
- Integration with authorized financial data providers.
- Downloadable monthly financial reports.

## 📄 License

This project is developed for academic and educational purposes. An open-source license may be added if the team intends to distribute the code publicly.

---

**SpendSense — Track Smarter. Budget Better. Spend Wisely.**
