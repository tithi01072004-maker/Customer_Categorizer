import sqlite3
import pandas as pd


# Create database connection
def create_connection():
    return sqlite3.connect("customers.db")


# Load CSV data into SQL table
def load_data():
    conn = create_connection()
    df = pd.read_csv("notebooks/data/clustered_data.csv")

    # Save dataframe as SQL table named "customers"
    df.to_sql("customers", conn, if_exists="replace", index=False)

    conn.close()


# Segment Summary
def get_segment_summary():
    conn = create_connection()

    query = """
    SELECT cluster,
           COUNT(*) AS total_customers,
           ROUND(AVG(Total_Spending), 2) AS avg_spending,
           ROUND(SUM(Total_Spending), 2) AS total_revenue
    FROM customers
    GROUP BY cluster
    ORDER BY total_revenue DESC
    """

    result = pd.read_sql(query, conn)
    conn.close()
    return result


# Spending vs Children analysis
def get_children_spending():
    conn = create_connection()

    query = """
    SELECT Children,
           ROUND(AVG(Total_Spending), 2) AS avg_spending
    FROM customers
    GROUP BY Children
    ORDER BY Children
    """

    result = pd.read_sql(query, conn)
    conn.close()
    return result


# For testing directly
if __name__ == "__main__":
    load_data()
    print(get_segment_summary())
    print(get_children_spending())