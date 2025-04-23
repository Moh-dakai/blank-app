import streamlit as st
import pandas as pd
from datetime import datetime
from data import (
    add_expense, add_income, load_data, load_income_data,
    get_summary_stats, get_monthly_breakdown, get_monthly_income_breakdown,
    plot_pie_chart
)

st.set_page_config(page_title="NairaGhibli App", layout="wide")

# Inject CSS to replicate UI from images
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to bottom, #fefaf2, #eae3ce);
        color: #3e3e3e;
    }
    .sidebar .sidebar-content {
        background-color: #f4f5dd;
        border-right: 2px solid #dadbc4;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton > button {
        background-color: #a37d42;
        color: white;
        border-radius: 10px;
        font-size: 16px;
        padding: 0.4em 1em;
    }
    .stButton > button:hover {
        background-color: #8e6835;
        color: white;
    }
    .stTextInput > div > input, .stNumberInput > div > input {
        background-color: #f9f5e9;
        border: 1px solid #d6caa4;
        border-radius: 10px;
        padding: 10px;
    }
    .stDataFrame, .stTable {
        background-color: #fffef5;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Simple session state login check
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #4e463c;'>Welcome to NairaGhibli</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #786d5d;'>Track your expenses with Naija flavor and Ghibli calm.</p>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("### Login to continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            if username == "demo" and password == "pass123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

else:
    # Sidebar
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #2f3e29;'>NairaGhibli</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 16px; color: #a8572a;'>Track with Naija flavor & Ghibli calm</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        navigation_option = st.radio("", ["Dashboard", "Add Expense", "Analytics", "Savings Health", "Budgets"], index=0)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-style: italic; font-size: 14px;'>\"Small daily savings grow like the baobab free.\"<br>— Nigerian Proverb</p>", unsafe_allow_html=True)

        st.subheader("Monthly Income")
        with st.form("income_form"):
            income_month = st.text_input("Month (YYYY-MM)")
            income_amt = st.number_input("Income Amount", min_value=0.0)
            income_submitted = st.form_submit_button("Save Income")
            if income_submitted:
                success, msg = add_income(income_month, income_amt)
                st.success(msg) if success else st.error(msg)

    st.markdown("<h1 style='text-align: center; color: #2f3e29;'>Financial Dashboard</h1>", unsafe_allow_html=True)

    if navigation_option == "Dashboard":
        summary = get_summary_stats()
        if summary:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Spent", f"₦{summary['total_spent']:,.0f}")
            with col2:
                this_month = datetime.now().strftime("%Y-%m")
                month_expenses = get_monthly_breakdown().get(this_month, 0)
                st.metric("This Month", f"₦{month_expenses:,.2f}")

        st.markdown("---")

        st.subheader("Recent Transactions")
        df = load_data()
        if not df.empty:
            df = df.sort_values(by="Date", ascending=False).head(5)
            st.dataframe(df.style.format({"Amount": "₦{:,.0f}"}))
        else:
            st.info("No recent transactions available.")

        st.markdown("---")

        st.subheader("Spending Distribution")
        tab1, tab2 = st.tabs(["By Category", "Over Time"])
        with tab1:
            plot_pie_chart()
        with tab2:
            st.info("Time-based distribution chart coming soon.")

    elif navigation_option == "Add Expense":
        st.subheader("Add New Expense")
        with st.form("expense_form_main"):
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            category = st.text_input("Category")
            note = st.text_input("Note (optional)")
            date = st.date_input("Date")
            description = st.text_input("Description")
            submitted = st.form_submit_button("Add Expense")
            if submitted:
                success, msg = add_expense(amount, category, note, date.strftime("%Y-%m-%d"), description)
                st.success(msg) if success else st.error(msg)

    elif navigation_option == "Analytics":
        st.subheader("Expense Breakdown")
        breakdown = get_monthly_breakdown()
        if breakdown:
            df = pd.DataFrame.from_dict(breakdown, orient='index', columns=['Total Spent'])
            st.bar_chart(df)
        else:
            st.info("No breakdown data to show.")

        st.subheader("Spending by Category")
        plot_pie_chart()

    elif navigation_option == "Savings Health":
        st.subheader("Savings Health")
        st.info("Savings health module coming soon.")

    elif navigation_option == "Budgets":
        st.subheader("Budgets")
        st.info("Budgets feature coming soon.") 
