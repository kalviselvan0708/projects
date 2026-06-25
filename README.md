# 📊 Sales Performance & Revenue Intelligence

> End-to-end business analytics project using Python, SQL, Excel, and Power BI  — analyzing 10,000+ sales transactions to uncover revenue trends, regional performance, and customer segments.

---

## 🗂️ Project Structure

```
sales-analysis/
├── data/
│   ├── generate_data.py          # Synthetic data generator
│   └── sample_sales_data.csv     # 9,994 rows of sales data (2021–2024)
├── sql/
│   └── queries.sql               # 12 business SQL queries
├── dashboard/
│   └── DASHBOARD_GUIDE.md        # Power BI & Tableau setup instructions
├── outputs/
│   ├── 01_revenue_dashboard.png  # Main KPI dashboard
│   ├── 02_regional_analysis.png  # Regional breakdown
│   ├── 03_discount_and_growth.png# Discount impact + YoY growth
│   ├── 04_rfm_segmentation.png   # Customer segmentation
│   └── sales_summary_report.xlsx # Multi-sheet Excel report
├── analysis.py                   # Main Python analysis script
├── requirements.txt
└── README.md
```

---

## 🔍 Business Questions Answered

| # | Question | Tool |
|---|----------|------|
| 1 | What are our monthly revenue and profit trends? | Python + SQL |
| 2 | Which regions and states drive the most revenue? | SQL + Power BI |
| 3 | How do discounts impact profitability? | Python |
| 4 | Which product categories/sub-categories are most profitable? | SQL + Tableau |
| 5 | Who are our most valuable customers? (RFM Analysis) | Python + SQL |
| 6 | What is our Year-over-Year revenue growth? | SQL |
| 7 | Which products are losing money? | SQL |
| 8 | How does shipping mode affect customer satisfaction? | SQL |

---

## 📈 Key Findings

- **$22.7M** in total revenue generated across 2021–2024
- **$3.6M** total profit with an average margin of **13.8%**
- **Technology** is the highest-revenue category; **Office Supplies** has the best margin
- High discounts (>30%) consistently result in negative profit — costing the business revenue
- **Champions** segment (top RFM customers) generates **~35%** of total revenue despite being <20% of customers
- The **West** region leads in both revenue and profit margin

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| **Python** | Data cleaning, EDA, visualization, RFM analysis |
| **pandas** | Data manipulation and feature engineering |
| **matplotlib / seaborn** | Charts and dashboards |
| **SQL** | Business queries, aggregations, window functions, CTEs |
| **Excel** | KPI summary report, pivot-ready output |
| **Power BI / Tableau** | Interactive dashboard (see `dashboard/DASHBOARD_GUIDE.md`) |

---

```


All charts and the Excel report will be saved in `/outputs/`.

### 5. SQL Queries
Open `sql/queries.sql` in any SQL client (MySQL Workbench, DBeaver, pgAdmin, or SQLite Browser).
Load `data/sample_sales_data.csv` into a table named `sales` and run any query.

### 6. Power BI / Tableau Dashboard
See `dashboard/DASHBOARD_GUIDE.md` for step-by-step setup instructions.

---


---

## 💼 Skills Demonstrated

- **Data Wrangling**: Handling 10K+ rows, feature engineering, date parsing
- **SQL**: CTEs, window functions (RANK, NTILE, LAG), aggregations, subqueries
- **EDA**: Distribution analysis, correlation study, outlier detection
- **Business Analytics**: RFM modelling, YoY growth, profitability analysis
- **Data Visualization**: Multi-chart dashboards, clear business storytelling
- **Excel Reporting**: Structured multi-sheet reports for stakeholders
- **BI Tools**: Power BI DAX measures, Tableau calculated fields

---

## 📁 Dataset

Synthetic data modelled after the [Kaggle Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).
Generated using `data/generate_data.py` — fully reproducible with a fixed random seed.

---

## 👤 Author

**[Your Name]**
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/kalviselvan08)
- GitHub: [github.com/yourusername](https://github.com/kalviselvan0708/projects)
- Email: kalviselvan0708@gmail.com

---

*Built as a portfolio project to demonstrate end-to-end data analysis skills.*
