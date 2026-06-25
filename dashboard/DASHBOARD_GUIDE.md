# Dashboard Setup Guide — Power BI & Tableau

## Data Source
Use `outputs/sales_summary_report.xlsx` (pre-cleaned, ready to connect).
Or connect directly to `data/sample_sales_data.csv`.

---

## Power BI Setup

### Steps
1. Open Power BI Desktop → **Get Data → Excel Workbook**
2. Select `sales_summary_report.xlsx`, import all sheets
3. In Power Query Editor: verify date columns are Date type, numeric columns are Decimal

### Suggested DAX Measures
```dax
Total Revenue    = SUM(sales[Sales])
Total Profit     = SUM(sales[Profit])
Profit Margin %  = DIVIDE([Total Profit], [Total Revenue]) * 100
Avg Order Value  = DIVIDE([Total Revenue], DISTINCTCOUNT(sales[Order ID]))

YoY Growth % =
VAR CurrYear = CALCULATE([Total Revenue], YEAR(sales[Order Date]) = YEAR(TODAY()))
VAR PrevYear = CALCULATE([Total Revenue], YEAR(sales[Order Date]) = YEAR(TODAY()) - 1)
RETURN DIVIDE(CurrYear - PrevYear, PrevYear) * 100
```

### Recommended Visuals

| Page | Visuals |
|------|---------|
| **Overview** | KPI cards (Revenue, Profit, Orders, Margin), Line chart (monthly revenue), Donut (category split) |
| **Regional** | Filled map (revenue by state), Bar chart (region comparison), Table (top states) |
| **Products** | Treemap (sub-category revenue), Scatter (discount vs profit), Bar (top 10 products) |
| **Customers** | Bar (RFM segments), Pie (segment revenue share), Table (top customers) |

---

## Tableau Setup

1. Open Tableau Desktop → **Connect → Text File** → select `sample_sales_data.csv`
2. Drag `Order Date` to Columns, `Sales` to Rows to verify connection

### Suggested Calculated Fields
```
// Profit Margin %
SUM([Profit]) / SUM([Sales]) * 100

// Days to Ship
DATEDIFF('day', [Order Date], [Ship Date])

// RFM Category (simplified)
IF SUM([Sales]) > 5000 THEN "High Value"
ELSEIF SUM([Sales]) > 2000 THEN "Mid Value"
ELSE "Low Value"
END
```

### Dashboard Layout
- **Sheet 1**: Monthly Revenue Line Chart (Year filter)
- **Sheet 2**: Region Performance Bar Chart
- **Sheet 3**: Category Treemap
- **Sheet 4**: Discount vs Profit Scatter Plot
- **Dashboard**: Combine all 4 with interlinked filters

---

## Free Alternatives (no license needed)
- **Metabase** (open source): connect to SQLite/PostgreSQL, drag-and-drop dashboards
- **Apache Superset**: enterprise-grade, free, supports all SQL databases
- **Google Looker Studio**: free, connects to Google Sheets/CSV via Google Drive
