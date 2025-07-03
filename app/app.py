import streamlit as st
import pandas as pd

# Load flagged ingredients dataset once
@st.cache_data
def load_flagged_data():
    return pd.read_csv("../data/flagged_ingredients.csv")

flagged_df = load_flagged_data()

st.title("NutriCheck AI - Ingredient Flagging Demo")

st.markdown("""
Enter ingredients separated by commas (like on a food label).  
The app will flag each ingredient as Excellent, Good, Bad, or Unknown.
""")

user_input = st.text_area("Paste ingredients here:", height=150)

if user_input:
    # Clean and split input into list of ingredients
    input_ingredients = [ing.strip().lower() for ing in user_input.split(",")]

    results = []

    for ing in input_ingredients:
        row = flagged_df[flagged_df["ingredient"].str.lower() == ing]
        if not row.empty:
            cat = row.iloc[0]["category"]
            reason = row.iloc[0]["reason"]
        else:
            cat = "Unknown"
            reason = "Not found in rulebook"

        results.append({"ingredient": ing, "category": cat, "reason": reason})

    result_df = pd.DataFrame(results)

    # Color code categories
    def color_category(val):
        if val == "Good":
            color = "yellow"
        elif val == "Bad":
            color = "red"
        elif val == "Excellent":
            color = "green"
        else:
            color = "lightgray"
        return f"background-color: {color}"

    st.write("### Flagged Ingredients")
    st.dataframe(result_df.style.applymap(color_category, subset=["category"]))

else:
    st.info("Please paste ingredients above to see their flagging.")
