import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import date

# --- 1. FILE PATHING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING & SELF-HEALING ---
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        # Create a full starter set if the file is completely missing
        starter_data = {
            "Date": [str(date.today())] * 3,
            "Store": ["Smith's (Kroger)", "Sprouts", "Food King"],
            "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
            "Price": [3.69, 4.49, 3.10]
        }
        df = pd.DataFrame(starter_data)
        df.to_csv(CSV_FILE, index=False)
    
    # FIX 1: Ensure 'Date' exists
    if 'Date' not in df.columns:
        df['Date'] = str(date.today())
    
    # FIX 2: Apply Food King 10% Math IMMEDIATELY so the column exists for the chart
    def calculate_total(row):
        if "food king" in str(row['Store']).lower():
            return round(row['Price'] * 1.10, 2)
        return row['Price']
    
    df['Checkout Total'] = df.apply(calculate_total, axis=1)
    
    # FIX 3: Convert Date to datetime objects for Plotly
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

df = load_data()

# --- 3. DASHBOARD UI ---
st.set_page_config(page_title="El Paso Price Tracker", page_icon="🌵", layout="wide")
st.title("🌵 El Paso Grocery Price History")

# Dropdown for Product Selection
all_items = sorted(df['Item'].unique())
selected_item = st.selectbox("Select a product to track:", all_items)

# Filter data for the chart
filtered_df = df[df['Item'] == selected_item].sort_values('Date')

# --- 4. LINE CHART ---
if not filtered_df.empty:
    # Use 'Checkout Total' which is now guaranteed to exist
    fig = px.line(
        filtered_df, 
        x="Date", 
        y="Checkout Total", 
        color="Store",
        title=f"Price Trend: {selected_item}",
        markers=True,
        labels={"Checkout Total": "Price ($)", "Date": "Collection Date"}
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No data found for '{selected_item}'.")

# --- 5. LATEST PRICES TABLE ---
st.divider()
st.subheader(f"Price History for {selected_item}")
table_df = filtered_df.sort_values('Date', ascending=False)
st.dataframe(table_df[['Date', 'Store', 'Price', 'Checkout Total']], use_container_width=True)

st.info("💡 Food King prices include the 10% 'Cost Plus' surcharge.")
