## SpendSense — Smart Budget Monitoring System with Threshold Alerts

**Capstone ID:** CP-002  
**Domain:** Banking and FinTech  
**Project Level:** Foundation

SpendSense is a personal finance management application that helps students and young professionals track their expenses, manage monthly budgets, and receive timely alerts before exceeding their spending limits.

The system provides category-wise expense analysis, budget utilization tracking, monthly spending summaries, and identification of the five largest expenses to encourage better financial decisions.

## 🎯 Objectives

- Track daily expenses with date, category, amount, and notes.
- Set monthly budgets for individual expense categories.
- Generate alerts when spending reaches 80% and 100% of a category's budget.
- Visualize monthly expenses against allocated budgets.
- Identify the five largest expenses of the selected month.
- Encourage responsible spending through transparent financial insights.

## ✨ Features

### 1. Expense Management
- Add expenses with date, category, amount, and description.
- View and manage recorded expenses.
- Organize transactions by month and category.

### 2. Monthly Budget Management
- Set a separate budget for each expense category.
- Track spending against allocated limits.
- Calculate remaining budget and utilization percentage.

### 3. Smart Threshold Alerts
- **80% threshold:** Notify users when a category approaches its budget limit.
- **100% threshold:** Notify users when spending reaches or exceeds the allocated budget.
- Prevent duplicate alerts for the same threshold crossing.

### 4. Monthly Summary Dashboard
- Display total monthly expenditure.
- Compare category-wise spending against budgets.
- Show budget utilization and remaining balances.
- Identify categories with high spending.

### 5. Top 5 Largest Expenses
- Retrieve the five highest-value expenses for the selected month.
- Sort expenses in descending order by amount.
- Display relevant transaction details.

## 🚀 Optional Enhancements

- Compare current-month and previous-month spending by category.
- Export monthly expenses to CSV.
- Interactive spending charts.
- User authentication and personalized dashboards.
- Responsive interface for mobile and desktop.
- Automated tests for budget calculations and threshold alerts.

## 🛠️ Technology Stack

The following is the proposed technology stack; update it if your implementation uses different technologies.

| Component | Technology |
|---|---|
| Frontend | React.js with Vite |
| Backend | Python with FastAPI |
| Database | PostgreSQL |
| Data Visualization | Recharts |
| API Testing | Postman |
| Automated Testing | Pytest |
| Version Control | Git and GitHub |

## 🏗️ System Architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  +----------------------+
  |                      |
  v                      v
Expense Management   Budget Management
  |                      |
  +-----------+----------+
              |
              v
       PostgreSQL Database
              |
              v
    Budget Calculation Engine
              |
              v
       Threshold Alerts
              |
              v
     Monthly Summary Dashboard
```

## 📊 Budget Calculation Logic

**Budget Utilization**

`Utilization (%) = (Category Spending / Category Budget) × 100`

**Remaining Budget**

`Remaining Budget = Category Budget − Category Spending`

Example:

| Category | Monthly Budget | Amount Spent | Utilization | Status |
|---|---:|---:|---:|---|
| Food | ₹3,000 | ₹1,500 | 50% | Within budget |
| Transport | ₹2,000 | ₹1,700 | 85% | 80% alert |
| Shopping | ₹2,500 | ₹2,600 | 104% | Budget exceeded |

*Illustrative data only.*

## 📁 Suggested Project Structure

```text
SpendSense/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── App.jsx
│   └── package.json
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
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

Install the following tools:

- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Git](https://git-scm.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/SpendSense.git
cd SpendSense
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Set Up the Backend

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

Configure the PostgreSQL database connection using environment variables or a local `.env` file.

Start the development server:

```bash
uvicorn app.main:app --reload
```

When the server starts successfully, open `http://127.0.0.1:8000/docs` to explore the API documentation.

### 3. Set Up the Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite in your terminal.

> These commands assume the proposed folder structure and technology stack. Adjust them to match the actual implementation.

## 🧪 Testing

Run backend tests from the `backend/` directory:

```bash
pytest
```

Important test scenarios include:

- Adding and retrieving expenses.
- Calculating category-wise monthly totals.
- Triggering alerts at 80% and 100%.
- Handling expenses that exceed a budget in one transaction.
- Sorting the five largest expenses correctly.
- Handling months with no expenses or no configured budget.
- Preventing unauthorized access to another user's financial records, if authentication is implemented.

## 🔒 Security Considerations

- Validate all expense amounts, dates, and categories.
- Use parameterized database queries or a secure ORM.
- Store credentials and secrets in environment variables.
- Never commit database passwords, API keys, or real financial records.
- Enforce server-side authorization for user-specific data.

## 🎓 Learning Outcomes

This project demonstrates practical application of:

- CRUD operations and REST API development.
- Relational database design.
- Aggregation and category-wise financial analysis.
- Sorting and date-based filtering.
- Threshold-based notification logic.
- Data visualization and dashboard design.
- Software testing, version control, and deployment.

## 🔮 Future Scope

- Personalized spending insights using machine learning.
- Recurring expense detection.
- Savings goal tracking.
- Automated transaction categorization.
- Integration with authorized financial data providers.

## 👩‍💻 Author

**Anjlee S**  
BE — Artificial Intelligence and Machine Learning  
Atria Institute of Technology

## 📄 License

This project is intended for educational and academic purposes. Add an appropriate open-source license if you plan to distribute the source code publicly.

---

**SpendSense — Track Smarter. Budget Better. Spend Wisely.**