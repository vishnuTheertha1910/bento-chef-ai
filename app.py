import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# --- Edamam Nutrition API ---
def get_nutrition_data(ingredients):
    url = "https://api.edamam.com/api/nutrition-data"
    params = {
        "app_id": os.getenv("85a5bbaa"),
        "app_key": os.getenv("c5e15c0327792f57782d9f04253d435f"),
        "ingr": ingredients  # Format: "100g chicken, 1 cup rice"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# --- App ---
st.title("🍱 Bento Chef AI (Edamam Free)")

# Simple login (demo only)
if "logged_in" not in st.session_state:
    if st.text_input("Enter Password", type="password") == "chef123":
        st.session_state.logged_in = True
    else:
        st.stop()

# Input Form
with st.form("input_form"):
    ingredients = st.text_input("Ingredients with quantities", "100g chicken, 50g rice")
    submitted = st.form_submit_button("Analyze & Generate")

if submitted:
    # Get nutrition data
    nutrition = get_nutrition_data(ingredients)
    
    if nutrition:
        # Extract macros
        protein = nutrition["totalNutrients"]["PROCNT"]["quantity"]
        fat = nutrition["totalNutrients"]["FAT"]["quantity"]
        carbs = nutrition["totalNutrients"]["CHOCDF"]["quantity"]
        
        # Display
        st.subheader("Macro Breakdown")
        st.write(f"Protein: {protein:.1f}g | Fat: {fat:.1f}g | Carbs: {carbs:.1f}g")
        st.bar_chart({"Protein": protein, "Fat": fat, "Carbs": carbs})
        
        # Generate simple recipe (no API)
        st.subheader("Suggested Recipe")
        st.write(f"""**Chicken Rice Bowl**
        - Mix {ingredients}
        - Season with spices
        - Bake at 180°C for 25 mins""")
    else:
        st.error("Failed to analyze ingredients")