import streamlit as st
import pandas as pd
import os

# --- 1. ROBUST FILE PATHING ---
# This ensures the app finds the CSV on GitHub/Streamlit Cloud regardless of the working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING ---
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        # If the file is missing, we create a helpful error for the user
        st.error(f"⚠️ Critical Error: '{os.path.basename(CSV_FILE)}' not found in the repository.")
        st.info("Please ensure you have uploaded the CSV file to the same folder as your app.py on GitHub.")
        st.stop()

df = load_data()

# --- 3. THE "EL PASO MATH" LOGIC ---
# We calculate the final checkout price, adding 10% for Food King items
def calculate_checkout_total(row):
    # Check if 'Food King' is in the store name (case insensitive)
    if "food king" in str(row['Store']).lower():
        return round(row['Price'] * 1.10, 2)
    return row['Price']

# Apply the math to create a new column
df['Checkout Total'] = df.apply(calculate_checkout_total, axis=1)

# --- 4. STREAMLIT DASHBOARD UI ---
st.set_page_config(page_title="El Paso Grocery Tracker", page_icon="🌵", layout="wide")

st.title("🌵 El Paso Grocery Price Tracker")
st.markdown("Comparing prices across **Smith's (Kroger)**, **Sprouts**, and **Food King**.")
st.caption("Data updates every Wednesday at 6:00 AM MST.")

# Create columns for high-level metrics
col1, col2 = st.columns(2)
with col1:
    st.subheader("Interactive Price List")
    # Highlight the cheapest Checkout Total in green
    st.dataframe(
        df.style.highlight_min(axis=0, subset=['Checkout Total'], color='#D4EDDA'),
        use_container_width=True
    )
    st.info("💡 **Note:** Food King prices automatically include the 10% 'Cost Plus' surcharge.")

with col2:
    st.subheader("Price Distribution by Store")
    # A bar chart to visualize who is cheapest for specific items
    st.bar_chart(data=df, x="Item", y="Checkout Total", color="Store")

# --- 5. DATA EXPORT OPTION ---
st.divider()
st.download_button(
    label="Download Current Price Data (CSV)",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="el_paso_grocery_prices.csv",
    mime="text/csv",
)
