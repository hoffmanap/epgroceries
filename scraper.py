import pandas as pd
import os
from datetime import date

CSV_FILE = "el_paso_grocery_comparison_sample.csv"

def run_weekly_scrape():
    # 1. Load existing history
    if os.path.exists(CSV_FILE):
        df_history = pd.read_csv(CSV_FILE)
    else:
        df_history = pd.DataFrame(columns=["Date", "Store", "Item", "Price"])

    # 2. This is where your live scraping or weekly updates happen
    # For now, update these numbers weekly, or insert your scraper function here!
    new_scraped_data = pd.DataFrame([
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

    # 3. Combine and deduplicate
    df_combined = pd.concat([df_history, new_scraped_data], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["Date", "Store", "Item"], keep="last")
    
    # 4. Save back to the repo
    df_combined.to_csv(CSV_FILE, index=False)
    print(f"Successfully appended data for {date.today()}")

if __name__ == "__main__":
    run_weekly_scrape()
