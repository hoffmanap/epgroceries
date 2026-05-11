import streamlit as st
import pandas as pd
import os
import plotly.express as px

# --- 1. FILE PATHING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING (SELF-HEALING & DATE-AWARE) ---
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        
        # FIX: If 'Date' column is missing, add today's date to all rows
        if 'Date' not in df.columns:
            from datetime import date
            df['Date'] = str(date.today())
            # Save it back so the error doesn't happen again
            df.to_csv(CSV_FILE, index=False)
            
        return df
    else:
        # Create a full starter set with the 'Date' column included
        from datetime import date
        starter_data = {
            "Date": [str(date.today())] * 3,
            "Store": ["Smith's (Kroger)", "Sprouts", "Food King"],
            "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
            "Price": [3.69, 4.49, 3.10]
        }
        df_starter = pd.DataFrame(starter_data)
        df_starter.to_csv(CSV_FILE, index=False)
        return df_starter

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
