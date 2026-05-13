import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import date

# --- 1. FILE PATHING ---
# Ensures the app finds the CSV on GitHub/Streamlit Cloud regardless of the environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING (APPEND & TRACK HISTORY) ---
def load_data():
    """
    Loads historical data and appends new records. 
    Prevents the 'snapshot' issue by stacking new data on top of old.
    """
    # 2.1 Load existing history or create a base if the file is missing
    if os.path.exists(CSV_FILE):
        df_history = pd.read_csv(CSV_FILE)
    else:
        # Starter data for the very first run (May 6, 2026)
        starter_data = {
            "Date": ["2026-05-06", "2026-05-06", "2026-05-06"],
            "Store": ["Smith's (Kroger)", "Sprouts", "Food King"],
            "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
            "Price": [3.69, 4.49, 3.10]
        }
        df_history = pd.DataFrame(starter_data)

    # 2.2 Define New Scraped Data for Today
    # In your workflow, this represents the current week's prices
    new_records = pd.DataFrame({
        "Date": [str(date.today())] * 3,
        "Store": ["Smith's (Kroger)", "Sprouts", "Food King"],
        "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
        "Price": [3.75, 4.55, 3.15] # Simulated price change for tracking
    })

    # 2.3 Append and Clean
    # Combine old + new, then drop duplicates so manual runs don't double-count a day
    df_combined = pd.concat([df_history, new_records], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["Date", "Store", "Item"], keep="last")
    
    # Save the updated history back to the CSV in the repository
    df_combined.to_csv(CSV_FILE, index=False)

    # 2.4 Apply El Paso Math & Formatting
    # Add 10% 'Cost Plus' surcharge for Food King
    df_combined['Checkout Total'] = df_combined.apply(
        lambda x: round(x['Price'] * 1.10, 2) if "food king" in str(x['Store']).lower() else x['Price'], 
        axis=1
    )
    
    # Convert Date column to actual datetime objects for proper charting
    df_combined['Date'] = pd.to_datetime(df_combined['Date'])
    
    return df_combined

# Load the dataframe
df = load_data()

# --- 3. DASHBOARD UI ---
st.set_page_config(page_title="EP Grocery Tracker", page_icon="🌵", layout="wide")
st.title("🌵 El Paso Grocery Price History")
st.markdown("Tracking regional housing affordability often starts with the cost of living—starting with the grocery shelf.")

# Dropdown for Product Selection
# This allows you to toggle between Milk, Eggs, etc., as you add more items
all_items = sorted(df['Item'].unique())
selected_item = st.selectbox("Select a product to track over time:", all_items)

# Filter data for the specific item
filtered_df = df[df['Item'] == selected_item].sort_values('Date')

# --- 4. PRICE TREND VISUALIZATION ---
if not filtered_df.empty:
    # Interactive Line Chart using Plotly
    fig = px.line(
        filtered_df, 
        x="Date", 
        y="Checkout Total", 
        color="Store",
        title=f"Price Trend: {selected_item}",
        markers=True,
        labels={"Checkout Total": "Price ($)", "Date": "Collection Date"},
        color_discrete_map={
            "Smith's (Kroger)": "#005EB8", 
            "Sprouts": "#006732", 
            "Food King": "#E31837"
        }
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No historical data found for '{selected_item}'.")

# --- 5. DATA TABLE ---
st.divider()
st.subheader(f"Raw Data: {selected_item}")

# Sort by newest date first for readability
table_df = filtered_df.sort_values('Date', ascending=False)
st.dataframe(
    table_df[['Date', 'Store', 'Price', 'Checkout Total']].style.format({"Price": "${:.2f}", "Checkout Total": "${:.2f}"}), 
    use_container_width=True
)

st.info("💡 **Note:** Food King totals include the 10% surcharge added at the register.")
