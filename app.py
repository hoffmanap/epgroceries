import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import date

# --- 1. FILE PATHING ---
# Ensures the app finds the CSV on GitHub or Streamlit Cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# --- 2. DATA LOADING (APPEND & TRACK HISTORY) ---
def load_data():
    """
    Loads historical data and appends new records for the current week.
    """
    # 2.1 Load existing history or create a base if the file is missing
    if os.path.exists(CSV_FILE):
        df_history = pd.read_csv(CSV_FILE)
    else:
        # Starter data for the initial run (May 6, 2026)
        starter_data = {
            "Date": ["2026-05-06"] * 3,
            "Store": ["Smith's (Kroger)", "Sprouts", "Food King"],
            "Item": ["Milk (1gal)", "Milk (1gal)", "Milk (1gal)"],
            "Price": [3.69, 4.49, 3.10]
        }
        df_history = pd.DataFrame(starter_data)

    # 2.2 Expanded Data for the Current Week (May 13, 2026)
    # Includes: Milk, Eggs, Bread, Chicken, Water, Apples, Butter, and Cheerios
    new_records = pd.DataFrame([
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Milk (1gal)", "Price": 3.75},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Milk (1gal)", "Price": 4.55},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Milk (1gal)", "Price": 3.15},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Eggs (Large, Dozen)", "Price": 2.49},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Eggs (Large, Dozen)", "Price": 3.99},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Eggs (Large, Dozen)", "Price": 2.15},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Bread (20oz)", "Price": 1.99},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Bread (20oz)", "Price": 3.29},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Bread (20oz)", "Price": 1.50},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Chicken Breast (1lb)", "Price": 4.99},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Chicken Breast (1lb)", "Price": 5.99},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Chicken Breast (1lb)", "Price": 3.90},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Water (1gal)", "Price": 1.25},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Water (1gal)", "Price": 1.50},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Water (1gal)", "Price": 0.99},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Apples (1lb)", "Price": 1.88},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Apples (1lb)", "Price": 2.49},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Apples (1lb)", "Price": 1.45},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Butter (1lb)", "Price": 4.49},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Butter (1lb)", "Price": 5.99},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Butter (1lb)", "Price": 3.99},
        {"Date": str(date.today()), "Store": "Smith's (Kroger)", "Item": "Cheerios (12oz)", "Price": 3.99},
        {"Date": str(date.today()), "Store": "Sprouts", "Item": "Cheerios (12oz)", "Price": 4.99},
        {"Date": str(date.today()), "Store": "Food King", "Item": "Cheerios (12oz)", "Price": 3.50},
    ])

    # 2.3 Merge and Clean History
    # Append the new week's data to the old, then remove duplicates
    df_combined = pd.concat([df_history, new_records], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["Date", "Store", "Item"], keep="last")
    
    # Save the updated history back to the CSV file
    df_combined.to_csv(CSV_FILE, index=False)

    # 2.4 Apply El Paso Math
    # Adds the 10% 'Cost Plus' surcharge for Food King locations
    df_combined['Checkout Total'] = df_combined.apply(
        lambda x: round(x['Price'] * 1.10, 2) if "food king" in str(x['Store']).lower() else x['Price'], 
        axis=1
    )
    
    # Convert 'Date' to datetime for correct line chart spacing
    df_combined['Date'] = pd.to_datetime(df_combined['Date'])
    
    return df_combined

# Initialize the data
df = load_data()

# --- 3. DASHBOARD UI ---
st.set_page_config(page_title="EP Grocery Tracker", page_icon="🌵", layout="wide")
st.title("🌵 El Paso Grocery Price History")
st.markdown("Tracking regional cost of living trends across Smith's, Sprouts, and Food King.")

# Dropdown for Product Selection
all_items = sorted(df['Item'].unique())
selected_item = st.selectbox("Select a product to track over time:", all_items)

# Filter data for the line chart
filtered_df = df[df['Item'] == selected_item].sort_values('Date')

# --- 4. PRICE TREND VISUALIZATION ---
if not filtered_df.empty:
    # Plotly line chart to visualize price movement
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
st.subheader(f"Raw Price History: {selected_item}")

# Display historical records with the newest at the top
table_df = filtered_df.sort_values('Date', ascending=False)
st.dataframe(
    table_df[['Date', 'Store', 'Price', 'Checkout Total']].style.format({"Price": "${:.2f}", "Checkout Total": "${:.2f}"}), 
    use_container_width=True
)

st.info("💡 **Note:** Food King totals include the 10% 'Cost Plus' surcharge.")
