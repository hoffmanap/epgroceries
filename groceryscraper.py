import streamlit as st
import pandas as pd

# Function to normalize prices
def calculate_true_price(price, store):
    if store == "Food King":
        # Food King adds 10% at the register
        return round(price * 1.10, 2)
    return price

st.title("El Paso Grocery Price Matcher")

# --- DATA ENTRY / FETCHING SIMULATION ---
# In your final version, these lists will be populated by your scraper scripts
raw_data = [
    {"Store": "Smith's (Kroger)", "Item": "Milk (1gal)", "Price": 3.69},
    {"Store": "Sprouts", "Item": "Milk (1gal)", "Price": 4.29},
    {"Store": "Food King", "Item": "Milk (1gal)", "Price": 3.10}, # Shelf price
]

processed_data = []
for entry in raw_data:
    true_price = calculate_true_price(entry['Price'], entry['Store'])
    processed_data.append({
        "Store": entry['Store'],
        "Item": entry['Item'],
        "Checkout Price": true_price,
        "Note": "+10% added" if entry['Store'] == "Food King" else "Standard"
    })

df = pd.DataFrame(processed_data)

# --- DISPLAY ---
st.subheader("Price Comparison (Checkout Total)")
st.dataframe(df.style.highlight_min(axis=0, subset=['Checkout Price'], color='#D4EDDA'))

st.info("💡 **Tip:** Food King prices automatically include the 10% surcharge for a fair comparison.")
