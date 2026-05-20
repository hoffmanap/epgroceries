import streamlit as st
import pandas as pd
import os
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "el_paso_grocery_comparison_sample.csv")

# Streamlit only READS the file now
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    
    # Apply Food King Math
    df['Checkout Total'] = df.apply(
        lambda x: round(x['Price'] * 1.10, 2) if "food king" in str(x['Store']).lower() else x['Price'], 
        axis=1
    )
    df['Date'] = pd.to_datetime(df['Date'])
else:
    st.error("Missing data file.")
    st.stop()

# --- DASHBOARD UI ---
st.set_page_config(page_title="EP Grocery Tracker", page_icon="🌵", layout="wide")
st.title("🌵 El Paso Grocery Price History")

all_items = sorted(df['Item'].unique())
selected_item = st.selectbox("Select a product to track over time:", all_items)
filtered_df = df[df['Item'] == selected_item].sort_values('Date')

if not filtered_df.empty:
    fig = px.line(
        filtered_df, x="Date", y="Checkout Total", color="Store",
        title=f"Price Trend: {selected_item}", markers=True,
        labels={"Checkout Total": "Price ($)", "Date": "Collection Date"},
        color_discrete_map={"Smith's (Kroger)": "#005EB8", "Sprouts": "#006732", "Food King": "#E31837"}
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader(f"Raw Price History: {selected_item}")
st.dataframe(filtered_df.sort_values('Date', ascending=False), use_container_width=True)
