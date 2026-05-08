import streamlit as st
import pandas as pd
import os

# --- CONFIGURATION ---
# This matches the file name in your GitHub repository
CSV_FILE = "el_paso_grocery_comparison_sample.csv"

# --- 1. DATA LOADING/FETCHING ---
# We check if the file exists. If it does, we load it. 
# In the future, your scraper script will update this file every Wednesday.
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    # Fallback if the file is missing
    st.error(f"Could not find {CSV_FILE}. Please make sure it is in your repository.")
    st.stop()

# --- 2. DATA PROCESSING (The Loop) ---
# We ensure the Food King math is applied to every row in the 'Price' column.
# This loop looks at each row and creates the 'Checkout_Price' we want.
processed_rows = []
for index, row in df.iterrows():
    raw_price = row['Price']
    store_name = row['Store']
    
    # Apply Food King 10% Surcharge
    if "Food King" in store_name:
        checkout_price = round(raw_price * 1.10, 2)
    else:
        checkout_price = raw_price
    
    processed_rows.append({
        "Store": store_name,
        "Item": row['Item'],
        "Shelf Price": raw_price,
        "Checkout Total": checkout_price
    })

# Create our final display DataFrame
final_df = pd.DataFrame(processed_rows)

# --- 3. STREAMLIT DISPLAY ---
st.set_page_config(page_title="El Paso Grocery Tracker", page_icon="🌵")

st.title("🌵 El Paso Grocery Price Tracker")
st.markdown(f"**Target City:** El Paso, TX | **Update Day:** Wednesday")

# Highlight the cheapest option for each item
st.subheader("Current Price Comparison")
st.dataframe(
    final_df.style.highlight_min(axis=0, subset=['Checkout Total'], color='#D4EDDA'),
    use_container_width=True
)

st.info("💡 **Note:** Food King prices include the mandatory 10% 'Cost Plus' surcharge.")

# Optional: Add a simple bar chart
st.bar_chart(data=final_df, x="Item", y="Checkout Total", color="Store")