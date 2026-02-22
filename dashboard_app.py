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
elif page == "Prediction":

    st.subheader("🤖 Predict Customer Segment")

    model = joblib.load("catboost_model.pkl")

    parental_status = st.selectbox("Parental Status", [0, 1])
    children = st.number_input("Children", 0, 5)
    spending = st.number_input("Total Spending")

    if st.button("Predict"):

        input_data = pd.DataFrame({
            "Parental Status": [parental_status],
            "Children": [children],
            "Total_Spending": [spending]
        })

        prediction = model.predict(input_data)

        st.success(f"Predicted Cluster: {int(prediction[0])}")