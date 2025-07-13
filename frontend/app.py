import streamlit as st
import pandas as pd
import os
import sys
import importlib.util

# 👇 Add Nutricheck-AI (parent) folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Import your RAG pipeline function
from rag.query_engine import ask_question

# 🚨 Load model_logic.py from app/ using full path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app/model_logic.py"))
spec = importlib.util.spec_from_file_location("model_logic", module_path)
model_logic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_logic)
flag_ingredients = model_logic.flag_ingredients

# 💅 Page Config
st.set_page_config(
    page_title="NutriCheck-AI",
    page_icon="🧪",
    layout="wide"
)

# 💡 Custom CSS Styling with Visual Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background-color: #f8f9fa;
        color: #2c3e50;
    }

    h1, h2, h3, h4 {
        color: #1abc9c;
    }

    .stButton>button {
        background-color: #2ecc71;
        color: white;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #27ae60;
    }

    .stFileUploader label, .stTextInput>div>div>input {
        background-color: white !important;
        color: #2c3e50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🧪 App Title
st.title("NutriCheck-AI: Ingredient Safety Checker")

# Layout with two columns
left_col, right_col = st.columns([2, 2])

# --- CSV Upload Section ---
with left_col.expander("📤 Upload Ingredients CSV", expanded=True):
    uploaded_file = st.file_uploader("Upload a CSV file with a column named 'ingredient':", type="csv")
    if uploaded_file:
        input_df = pd.read_csv(uploaded_file)
        uploaded_path = "../data/user_uploaded.csv"
        input_df.to_csv(uploaded_path, index=False)

        st.success("CSV uploaded successfully!")
        output_path = "../data/flagged_results.csv"

        flag_ingredients(
            input_csv=uploaded_path,
            rules_csv="../data/ingredient_rules_large.csv",
            output_csv=output_path
        )

        result_df = pd.read_csv(output_path)
        st.session_state["flagged_df"] = result_df
        st.dataframe(result_df, use_container_width=True)

        # 📊 Summary Chart
        st.subheader("📊 Ingredient Category Summary")
        category_counts = result_df['category'].value_counts()
        chart_type = st.radio("Choose chart type:", ["Pie Chart", "Bar Chart"])

        if chart_type == "Pie Chart":
            st.plotly_chart({
                "data": [{
                    "values": category_counts.values.tolist(),
                    "labels": category_counts.index.tolist(),
                    "type": "pie"
                }]
            }, use_container_width=True)

        elif chart_type == "Bar Chart":
            st.bar_chart(category_counts)

        # 💾 Download flagged CSV
        st.subheader("💾 Download Flagged Results")
        csv_download = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_download,
            file_name="flagged_ingredients.csv",
            mime="text/csv"
        )

# --- Label Image Upload ---
with left_col.expander("🖼️ Upload Food Label Image (Future Feature)", expanded=False):
    image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if image_file:
        st.image(image_file, caption="Uploaded Label", use_column_width=True)

# --- Query Ingredient Section ---
with right_col.expander("🤖 Ask a Question about an Ingredient", expanded=True):
    user_query = st.text_input("Type your question here:")
    if user_query:
        answer = ask_question(user_query)
        st.markdown("**Answer:**")
        st.write(answer)
