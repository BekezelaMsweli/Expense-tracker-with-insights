import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Dashboard", layout="wide")

st.title("💰 Personal Expense Dashboard")

# ================== LOAD DATA ==================
df = pd.read_csv("Expenses.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period("M")

# ================== CATEGORIZE ==================
def categorize(desc):
    desc = str(desc).lower()
    if "grocery" in desc or "restaurant" in desc:
        return "Food"
    elif "transport" in desc:
        return "Transport"
    elif "rent" in desc:
        return "Housing"
    elif "electricity" in desc or "internet" in desc:
        return "Utilities"
    elif "salary" in desc:
        return "Income"
    else:
        return "Other"

df['category'] = df['description'].apply(categorize)

income_df = df[(df['amount'] > 0) & (df['category'] == "Income")]
expenses_df = df[df['amount'] < 0].copy()
expenses_df['amount'] = expenses_df['amount'].abs()

monthly_income = income_df.groupby('month')['amount'].sum()
monthly_expenses = expenses_df.groupby('month')['amount'].sum()
monthly_savings = monthly_income - monthly_expenses
category_spending = expenses_df.groupby('category')['amount'].sum()

# ================== KPI ROW (TOP SECTION) ==================
col1, col2, col3 = st.columns(3)

col1.metric("Income", f"R{monthly_income.sum():,.0f}")
col2.metric("Expenses", f"R{monthly_expenses.sum():,.0f}")
col3.metric("Savings", f"R{monthly_savings.sum():,.0f}")

st.markdown("---")

# ================== 🔥 KEY INSIGHTS ==================
st.subheader("📌 Key Insights")

avg_savings = monthly_savings.mean()
highest_category = category_spending.idxmax()
highest_spend = category_spending.max()

income_trend = monthly_income.pct_change().mean() * 100
expense_trend = monthly_expenses.pct_change().mean() * 100

st.markdown(f"""
- 💡 Your **highest spending category** is **{highest_category}** (R{highest_spend:,.0f})
- 💰 Your **average monthly savings** is **R{avg_savings:,.0f}**
- 📈 Average income change per month: **{income_trend:.1f}%**
- 📉 Average expense change per month: **{expense_trend:.1f}%**
""")

# ================== 🔥 MIDDLE SECTION (2 COLUMNS) ==================
col4, col5 = st.columns(2)

with col4:
    st.subheader("Spending by Category")
    fig1, ax1 = plt.subplots(figsize=(3,3))
    category_spending.plot(kind='pie', autopct='%1.1f%%', ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

with col5:
    st.subheader("Monthly Savings Trend")
    fig2, ax2 = plt.subplots(figsize=(4,3))
    monthly_savings.plot(kind='line', marker='o', ax=ax2)
    st.pyplot(fig2)

# ================== 🔥 BOTTOM SECTION (FULL WIDTH) ==================
st.subheader("Monthly Expenses")

fig3, ax3 = plt.subplots(figsize=(10,3))
monthly_expenses.plot(kind='bar', ax=ax3)

for bar in ax3.patches:
    ax3.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"R{bar.get_height():,.0f}",
        ha='center',
        va='bottom',
        fontsize=8
    )

st.pyplot(fig3)