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

st.title("NutriCheck-AI: Ingredient Safety Checker")

# Upload CSV of ingredients
st.subheader("📤 Upload Ingredients CSV")
uploaded_file = st.file_uploader("Upload a CSV file with a column named 'ingredient':", type="csv")

# Optional: Upload image (for future OCR support)
st.subheader("🖼️ Upload an image of a food label (experimental)")
image_file = st.file_uploader("Upload a food label image", type=["png", "jpg", "jpeg"])

# Process uploaded CSV
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    
    # Save the uploaded file to data folder
    uploaded_path = "../data/user_uploaded.csv"
    input_df.to_csv(uploaded_path, index=False)
    
    st.success("CSV uploaded and saved. Flagging ingredients...")

    # Run the flagging logic
    output_path = "../data/flagged_results.csv"
    flag_ingredients(input_csv=uploaded_path, 
                     rules_csv="../data/ingredient_rules_large.csv",
                     output_csv=output_path)

    # Load and display results
    result_df = pd.read_csv(output_path)
    st.dataframe(result_df)

    st.session_state["flagged_df"] = result_df  # store for later use

    # 📊 Visual summary
    st.subheader("📊 Ingredient Category Summary")
    category_counts = result_df['category'].value_counts()
    st.write(category_counts)

    chart_type = st.radio("Choose chart type:", ["Pie Chart", "Bar Chart"])

    if chart_type == "Pie Chart":
        st.plotly_chart(
            {
                "data": [
                    {
                        "values": category_counts.values.tolist(),
                        "labels": category_counts.index.tolist(),
                        "type": "pie"
                    }
                ]
            },
            use_container_width=True
        )

    elif chart_type == "Bar Chart":
        st.bar_chart(category_counts)

# --- New Section for RAG Q&A ---
st.subheader("🤖 Ask a Question about an Ingredient")

user_query = st.text_input("Type your question here:")

if user_query:
    with st.spinner("Getting answer from NutriCheck-AI..."):
        from rag.query_engine import ask_question  # adjust path if needed
        answer = ask_question(user_query)
    st.markdown("### Answer:")
    st.write(answer)

