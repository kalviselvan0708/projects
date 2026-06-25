"""
Sales Performance & Revenue Intelligence Analysis
=================================================
Full EDA + Business Insights using Python (pandas, matplotlib, seaborn)

Author: [Your Name]
Dataset: Superstore-style Sales Data (2021–2024)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

# ── Color palette ──────────────────────────────────────────────────────────────
COLORS = {
    "primary": "#2563EB",
    "accent":  "#F59E0B",
    "danger":  "#EF4444",
    "success": "#10B981",
    "neutral": "#6B7280",
    "bg":      "#F8FAFC",
}
PALETTE = [COLORS["primary"], COLORS["accent"], COLORS["success"], COLORS["danger"], COLORS["neutral"]]

plt.rcParams.update({
    "figure.facecolor": COLORS["bg"],
    "axes.facecolor":   COLORS["bg"],
    "axes.spines.top":  False,
    "axes.spines.right":False,
    "font.family":      "DejaVu Sans",
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
    "axes.labelsize":   11,
})

# ── 1. Load & clean ────────────────────────────────────────────────────────────
print("=" * 60)
print("  SALES PERFORMANCE & REVENUE INTELLIGENCE ANALYSIS")
print("=" * 60)

df = pd.read_csv("data/sample_sales_data.csv", parse_dates=["Order Date", "Ship Date"])

# Feature engineering
df["Year"]          = df["Order Date"].dt.year
df["Month"]         = df["Order Date"].dt.month
df["Month Name"]    = df["Order Date"].dt.strftime("%b")
df["Quarter"]       = df["Order Date"].dt.to_period("Q").astype(str)
df["Profit Margin"] = (df["Profit"] / df["Sales"]).replace([np.inf, -np.inf], np.nan)
df["Ship Days"]     = (df["Ship Date"] - df["Order Date"]).dt.days

print(f"\n📦 Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
print(f"   Date range: {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
print(f"   Missing values: {df.isnull().sum().sum()}")

# ── 2. KPI Summary ─────────────────────────────────────────────────────────────
total_sales    = df["Sales"].sum()
total_profit   = df["Profit"].sum()
total_orders   = df["Order ID"].nunique()
avg_margin     = df["Profit Margin"].mean() * 100
avg_order_val  = total_sales / total_orders

print("\n📊 KEY PERFORMANCE INDICATORS")
print(f"   Total Revenue    : ${total_sales:>12,.2f}")
print(f"   Total Profit     : ${total_profit:>12,.2f}")
print(f"   Unique Orders    : {total_orders:>12,}")
print(f"   Avg Order Value  : ${avg_order_val:>12,.2f}")
print(f"   Avg Profit Margin: {avg_margin:>11.1f}%")

# ── 3. Revenue trend (monthly) ─────────────────────────────────────────────────
monthly = (df.groupby(["Year", "Month"])
             .agg(Revenue=("Sales", "sum"), Profit=("Profit", "sum"))
             .reset_index())
monthly["Date"] = pd.to_datetime(monthly[["Year", "Month"]].assign(day=1))
monthly = monthly.sort_values("Date")

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle("Sales Performance & Revenue Intelligence Dashboard", fontsize=16, fontweight="bold", y=1.01)

# Plot 1 — Monthly revenue trend
ax = axes[0, 0]
ax.plot(monthly["Date"], monthly["Revenue"], color=COLORS["primary"], linewidth=2.5, zorder=3)
ax.fill_between(monthly["Date"], monthly["Revenue"], alpha=0.12, color=COLORS["primary"])
ax.plot(monthly["Date"], monthly["Profit"],  color=COLORS["success"], linewidth=2, linestyle="--", zorder=3)
ax.set_title("Monthly Revenue vs Profit (2021–2024)")
ax.set_xlabel("")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.legend(["Revenue", "Profit"], frameon=False)

# Plot 2 — Sales by Category & Sub-category
ax = axes[0, 1]
cat_sales = df.groupby("Category")["Sales"].sum().sort_values()
bars = ax.barh(cat_sales.index, cat_sales.values, color=PALETTE[:3], edgecolor="white", linewidth=0.5)
ax.set_title("Total Revenue by Category")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
for bar, val in zip(bars, cat_sales.values):
    ax.text(val + 5000, bar.get_y() + bar.get_height()/2,
            f"${val/1e6:.2f}M", va="center", fontsize=9, color=COLORS["neutral"])

# Plot 3 — Top 10 Sub-categories by Revenue
ax = axes[1, 0]
sub_sales = df.groupby("Sub-Category")["Sales"].sum().nlargest(10).sort_values()
bars = ax.barh(sub_sales.index, sub_sales.values, color=COLORS["primary"], alpha=0.85, edgecolor="white")
ax.set_title("Top 10 Sub-Categories by Revenue")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))

# Plot 4 — Profit margin by Segment
ax = axes[1, 1]
seg_margin = df.groupby("Segment")["Profit Margin"].mean() * 100
seg_colors = [COLORS["primary"], COLORS["accent"], COLORS["success"]]
bars = ax.bar(seg_margin.index, seg_margin.values, color=seg_colors, edgecolor="white", linewidth=0.5)
ax.set_title("Avg Profit Margin by Customer Segment")
ax.set_ylabel("Profit Margin (%)")
ax.axhline(avg_margin, color=COLORS["danger"], linestyle="--", linewidth=1.2, label=f"Overall avg: {avg_margin:.1f}%")
ax.legend(frameon=False)
for bar, val in zip(bars, seg_margin.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f"{val:.1f}%",
            ha="center", va="bottom", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/01_revenue_dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n✅ Saved: outputs/01_revenue_dashboard.png")

# ── 4. Regional Analysis ───────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

region_kpis = df.groupby("Region").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
).reset_index()
region_kpis["Margin"] = region_kpis["Profit"] / region_kpis["Revenue"] * 100

ax = axes[0]
x = np.arange(len(region_kpis))
w = 0.35
ax.bar(x - w/2, region_kpis["Revenue"]/1e3, w, label="Revenue ($K)", color=COLORS["primary"], alpha=0.9)
ax.bar(x + w/2, region_kpis["Profit"]/1e3,  w, label="Profit ($K)",  color=COLORS["success"], alpha=0.9)
ax.set_xticks(x); ax.set_xticklabels(region_kpis["Region"])
ax.set_title("Revenue & Profit by Region")
ax.set_ylabel("Amount ($K)")
ax.legend(frameon=False)

ax = axes[1]
ax.bar(region_kpis["Region"], region_kpis["Margin"], color=PALETTE, edgecolor="white")
ax.set_title("Profit Margin % by Region")
ax.set_ylabel("Margin (%)")
ax.axhline(avg_margin, color=COLORS["danger"], linestyle="--", linewidth=1.2)
for i, (_, row) in enumerate(region_kpis.iterrows()):
    ax.text(i, row["Margin"] + 0.3, f"{row['Margin']:.1f}%", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/02_regional_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Saved: outputs/02_regional_analysis.png")

# ── 5. Discount Impact Analysis ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
disc_impact = df.groupby("Discount").agg(Profit=("Profit", "mean"), Sales=("Sales", "mean")).reset_index()
ax.scatter(df["Discount"], df["Profit"], alpha=0.03, color=COLORS["primary"], s=15)
ax.plot(disc_impact["Discount"], disc_impact["Profit"], color=COLORS["danger"], linewidth=2.5, label="Avg Profit")
ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
ax.set_title("Discount Rate vs Profit")
ax.set_xlabel("Discount Rate")
ax.set_ylabel("Profit ($)")
ax.legend(frameon=False)

ax = axes[1]
yoy = df.groupby("Year")["Sales"].sum()
growth = yoy.pct_change() * 100
colors_g = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in growth.dropna()]
ax.bar(growth.dropna().index, growth.dropna().values, color=colors_g, edgecolor="white")
ax.set_title("Year-over-Year Revenue Growth (%)")
ax.set_ylabel("Growth (%)")
ax.axhline(0, color="black", linewidth=0.8)
for i, (yr, val) in enumerate(growth.dropna().items()):
    ax.text(yr, val + 0.5 if val >= 0 else val - 2, f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/03_discount_and_growth.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Saved: outputs/03_discount_and_growth.png")

# ── 6. RFM Customer Segmentation ──────────────────────────────────────────────
snapshot = df["Order Date"].max() + pd.Timedelta(days=1)
rfm = df.groupby("Customer ID").agg(
    Recency  =("Order Date", lambda x: (snapshot - x.max()).days),
    Frequency=("Order ID",   "nunique"),
    Monetary =("Sales",      "sum"),
).reset_index()

rfm["R_Score"] = pd.qcut(rfm["Recency"],   5, labels=[5,4,3,2,1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"],  5, labels=[1,2,3,4,5]).astype(int)
rfm["RFM_Score"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

def rfm_segment(score):
    if score >= 13:  return "Champions"
    elif score >= 10: return "Loyal Customers"
    elif score >= 7:  return "Potential Loyalists"
    elif score >= 5:  return "At Risk"
    else:             return "Lost"

rfm["Segment"] = rfm["RFM_Score"].apply(rfm_segment)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

seg_counts = rfm["Segment"].value_counts()
seg_colors_map = {
    "Champions": COLORS["success"],
    "Loyal Customers": COLORS["primary"],
    "Potential Loyalists": COLORS["accent"],
    "At Risk": COLORS["danger"],
    "Lost": COLORS["neutral"],
}
ax = axes[0]
bars = ax.bar(seg_counts.index, seg_counts.values,
              color=[seg_colors_map.get(s, "#999") for s in seg_counts.index],
              edgecolor="white")
ax.set_title("RFM Customer Segmentation")
ax.set_ylabel("Number of Customers")
ax.set_xticklabels(seg_counts.index, rotation=20, ha="right")
for bar, val in zip(bars, seg_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 1, str(val), ha="center", fontsize=10, fontweight="bold")

ax = axes[1]
seg_revenue = rfm.merge(
    df.groupby("Customer ID")["Sales"].sum().reset_index(), on="Customer ID"
).groupby("Segment")["Sales"].sum().sort_values(ascending=False)
ax.pie(seg_revenue.values,
       labels=seg_revenue.index,
       colors=[seg_colors_map.get(s, "#999") for s in seg_revenue.index],
       autopct="%1.1f%%", startangle=140,
       wedgeprops={"edgecolor": "white", "linewidth": 1.5})
ax.set_title("Revenue Share by Customer Segment")

plt.tight_layout()
plt.savefig("outputs/04_rfm_segmentation.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Saved: outputs/04_rfm_segmentation.png")

# ── 7. Export to Excel ─────────────────────────────────────────────────────────
with pd.ExcelWriter("outputs/sales_summary_report.xlsx", engine="openpyxl") as writer:
    # KPI sheet
    kpi_data = {
        "Metric": ["Total Revenue", "Total Profit", "Unique Orders", "Avg Order Value", "Avg Profit Margin"],
        "Value": [f"${total_sales:,.2f}", f"${total_profit:,.2f}", f"{total_orders:,}",
                  f"${avg_order_val:,.2f}", f"{avg_margin:.1f}%"]
    }
    pd.DataFrame(kpi_data).to_excel(writer, sheet_name="KPIs", index=False)

    # Monthly trend
    monthly[["Date", "Revenue", "Profit"]].to_excel(writer, sheet_name="Monthly Trend", index=False)

    # Region
    region_kpis.to_excel(writer, sheet_name="Regional Analysis", index=False)

    # RFM
    rfm[["Customer ID", "Recency", "Frequency", "Monetary", "RFM_Score", "Segment"]].to_excel(
        writer, sheet_name="RFM Segments", index=False)

    # Category breakdown
    df.groupby(["Category", "Sub-Category"]).agg(
        Revenue=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")
    ).reset_index().to_excel(writer, sheet_name="Category Breakdown", index=False)

print("✅ Saved: outputs/sales_summary_report.xlsx")

print("\n🎉 Analysis complete! All outputs saved to /outputs/")
print("   → 01_revenue_dashboard.png")
print("   → 02_regional_analysis.png")
print("   → 03_discount_and_growth.png")
print("   → 04_rfm_segmentation.png")
print("   → sales_summary_report.xlsx")
