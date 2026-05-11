import streamlit as st
import pandas as pd
import plotly.express as px  # Make sure this is in your requirements.txt!
import os

# --- 1. DATA LOADING ---
CSV_FILE = "el_paso_grocery_comparison_sample.csv"
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date']) # Crucial for the line chart
else:
    st.error("CSV not found!")
    st.stop()

# --- 2. DATA PROCESSING (Calculations) ---
# ... (Your existing loop that adds the 10% for Food King) ...

# ---------------------------------------------------------
# --- 3. THE NEW VISUALIZATION (INSERT HERE) ---
# ---------------------------------------------------------
st.title("📈 El Paso Grocery Price Trends")

# Filter by Item so the line chart isn't messy
item_to_plot = st.selectbox("Select Item to Track", df['Item'].unique())
filtered_df = df[df['Item'] == item_to_plot]

# Create the Line Chart
fig = px.line(
    filtered_df, 
    x="Date", 
    y="Checkout_Price", 
    color="Store",
    title=f"Price History: {item_to_plot}",
    markers=True
)
st.plotly_chart(fig, use_container_width=True)
# ---------------------------------------------------------

# --- 4. DATA TABLE (Keep this at the bottom) ---
st.subheader("Raw Price Data")
st.dataframe(filtered_df)
