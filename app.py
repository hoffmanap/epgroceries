import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- 1. FILE PATHING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING & EL PASO MATH ---
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        # Create a starter set with historical dates if file is missing
        data = {
            "Date": ["2026-05-06", "2026-05-06", "2026-05-06", "2026-05-13", "2026-05-13", "2026-05-13"],
            "Store": ["Smith's (Kroger)", "Sprouts", "Food King", "Smith's (Kroger)", "Sprouts", "Food King"],
            "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)", "Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
            "Price": [3.69, 4.49, 3.10, 3.75, 4.55, 3.15]
        }
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False)
    
    # Apply Food King 10% Math
    df['Checkout Total'] = df.apply(
        lambda x: round(x['Price'] * 1.10, 2) if "food king" in str(x['Store']).lower() else x['Price'], 
        axis=1
    )
    # Ensure Date is actually a datetime object for the chart
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# --- 3. DASHBOARD UI ---
st.set_page_config(page_title="El Paso Price Tracker", page_icon="🌵", layout="wide")
st.title("🌵 El Paso Grocery Price History")

# Dropdown for Product Selection
all_items = sorted(df['Item'].unique())
selected_item = st.selectbox("Select a product to track:", all_items)

# Filter data for the chart and table
filtered_df = df[df['Item'] == selected_item].sort_values('Date')

# --- 4. LINE CHART ---
if not filtered_df.empty:
    fig = px.line(
        filtered_df, 
        x="Date", 
        y="Checkout Total", 
        color="Store",
        title=f"Price Trend: {selected_item}",
        markers=True,
        labels={"Checkout Total": "Price ($)", "Date": "Collection Date"}
    )
    # Clean up chart layout
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for the selected item.")

# --- 5. LATEST PRICES TABLE ---
st.divider()
st.subheader(f"Price History for {selected_item}")

# Sort by newest date first for the table
table_df = filtered_df.sort_values('Date', ascending=False)
st.dataframe(table_df[['Date', 'Store', 'Price', 'Checkout Total']], use_container_width=True)

st.info("💡 Food King prices include the 10% 'Cost Plus' surcharge.")
