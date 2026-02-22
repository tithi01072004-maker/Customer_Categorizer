import streamlit as st
import pandas as pd
import joblib
from sql import load_data, get_segment_summary, get_children_spending

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")

st.title("📊 Customer Segmentation Intelligence System")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Segment Analysis", "Prediction"])

# Load SQL Data
load_data()
segment_data = get_segment_summary()
children_data = get_children_spending()

# ---------------- OVERVIEW ----------------
if page == "Overview":

    st.subheader("📌 Business KPIs")

    col1, col2, col3 = st.columns(3)

    total_customers = segment_data["total_customers"].sum()
    total_revenue = segment_data["total_revenue"].sum()
    avg_spending = round(segment_data["avg_spending"].mean(), 2)

    col1.metric("Total Customers", total_customers)
    col2.metric("Total Revenue", f"${total_revenue:,.2f}")
    col3.metric("Average Spending", f"${avg_spending}")

# ---------------- SEGMENT ANALYSIS ----------------
elif page == "Segment Analysis":

    st.subheader("📈 Revenue by Segment")

    selected_cluster = st.selectbox(
        "Select Cluster",
        segment_data["cluster"]
    )

    filtered = segment_data[segment_data["cluster"] == selected_cluster]

    st.dataframe(filtered)

    st.bar_chart(segment_data.set_index("cluster")["total_revenue"])

    st.subheader("👨‍👩‍👧 Spending vs Children")
    st.bar_chart(children_data.set_index("Children")["avg_spending"])

# ---------------- PREDICTION ----------------
# ---------------- PREDICTION ----------------
elif page == "Prediction":

    st.subheader("🤖 Predict Customer Segment")

    model = joblib.load("catboost_updated.pkl")

    st.markdown("### Customer Profile")

    col1, col2, col3 = st.columns(3)

    age = col1.number_input("Age", 18, 100)

    # Education Mapping
    education_label = col2.selectbox(
        "Education",
        ["Basic", "Graduation", "Master", "PhD", "2n Cycle"]
    )

    education_map = {
        "Basic": 0,
        "Graduation": 1,
        "Master": 2,
        "PhD": 3,
        "2n Cycle": 4
    }

    education = education_map[education_label]

    # Marital Status Mapping
    marital_label = col3.selectbox(
        "Marital Status",
        ["Single", "Married"]
    )

    marital_map = {
        "Single": 0,
        "Married": 1
    }

    marital = marital_map[marital_label]

    # Parental Status Mapping
    parental_label = st.selectbox(
        "Parental Status",
        ["No Children", "Has Children"]
    )

    parental_map = {
        "No Children": 0,
        "Has Children": 1
    }

    parental_status = parental_map[parental_label]

    children = st.number_input("Children", 0, 5)

    income = st.number_input("Income")
    spending = st.number_input("Total Spending")

    st.markdown("### Customer Behaviour")

    col1, col2, col3 = st.columns(3)

    days_customer = col1.number_input("Days As Customer")
    recency = col2.number_input("Recency")
    web_visits = col3.number_input("Web Visits Per Month")

    st.markdown("### Product Spending")

    col1, col2, col3 = st.columns(3)

    wines = col1.number_input("Wine Spending ($)", min_value=0)
    fruits = col2.number_input("Fruit Spending ($)", min_value=0)
    meat = col3.number_input("Meat Spending ($)", min_value=0)

   
    fish = col1.number_input("Fish Spending ($)", min_value=0)
    sweets = col2.number_input("Sweets Spending ($)", min_value=0)
    gold = col3.number_input("Gold Products Spending ($)", min_value=0)
    st.markdown("### Purchase Channels")

    col1, col2, col3 = st.columns(3)

    web = col1.number_input("Web Purchases")
    catalog = col2.number_input("Catalog Purchases")
    store = col3.number_input("Store Purchases")

    discount = st.number_input("Discount Purchases")
    promo = st.number_input("Promotions Accepted")

    if st.button("Predict"):

        input_data = pd.DataFrame({
            "Age":[age],
            "Education":[education],
            "Marital_Status":[marital],
            "Parental Status":[parental_status],
            "Children":[children],
            "Income":[income],
            "Total_Spending":[spending],
            "Days_As_Customer":[days_customer],
            "Recency":[recency],
            "Wines":[wines],
            "Fruits":[fruits],
            "Meat":[meat],
            "Fish":[fish],
            "Sweets":[sweets],
            "Gold":[gold],
            "Web":[web],
            "Catalog":[catalog],
            "Store":[store],
            "Discount Purchases":[discount],
            "Total Promo":[promo],
            "NumWebVisitsMonth":[web_visits]
        })

        # Ensure correct feature order
        input_data = input_data[model.feature_names_]

        prediction = model.predict(input_data)
        cluster_names = {
            0: "Low Value Customers",
            1: "Medium Value Customers",
            2: "High Value Customers"
        }

        cluster_result = int(prediction[0])

        st.success(f"Cluster {cluster_result}: {cluster_names[cluster_result]}")