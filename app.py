import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests
from config import API_KEY

def main():
    st.title("My Fitness App")
    st.subheader("Powered by Health API")
    st.info("Input your fitness data and collect your caloric needs!")

    home, calc = st.tabs(['Home', 'Calculator'])

    with home:
        st.header("Welcome to My Fitness App!")
        st.markdown("""
        Use the **Fitness Calculator** tab to:
        - Input your age, height, and weight
        - Choose your goals and activity level
        - (Optional) Select diet & climate preferences

        Then click **Submit** to view your recommendations!
        """)

    with calc:
        st.header("Calorie Calculator")

        col1, col2 = st.columns(2)
        with col1:
            sex = st.selectbox("Sex", ("Male", "Female"))
            age = st.number_input("Age", min_value=1, max_value=80, value=25)
        with col2:
            unit = st.selectbox("Units", ("Metric (kg, cm)", "Imperial (lb, in)"))
            user = st.radio("User Mode", options=("Basic", "Advanced"), horizontal=True)

        if unit == "Imperial (lb, in)":
            height = st.number_input("Enter your height (in): ", key=4)
            weight = st.number_input("Enter your weight (lb): ", key=5)
        else:
            height = st.number_input("Enter your height (cm): ", key=6)
            weight = st.number_input("Enter your weight (kg): ", key=7)

        level = st.select_slider("Activity Level: ", (
            "Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"
        ), value="Moderately Active", key=8)

        goal = st.selectbox("Fitness Goal: ", ("Cut", "Maintain", "Bulk"), index=1, key=9)

        diet = None
        climate = "Average"
        if user == "Advanced":
            with st.expander("Advanced Options"):
                diet = st.selectbox("Dietary Preference:", (
                    "Regular", "Vegetarian", "Vegan", "Gluten-Free", "Pescatarian"
                ), key=10)
                climate = st.select_slider("Climate (for water intake):",
                                           ("Cold", "Average", "Hot"), value="Average", key=11)

        height = float(height)
        weight = float(weight)
        if unit == "Imperial (lb, in)":
            height *= 2.54
            weight *= 0.4536

        level_json, goal_json, diet_json, climate_json = maps(level, goal, diet, climate)

        submitted = st.button("Submit", key=12)
        if submitted:
            with st.spinner("Calculating your personalized caloric fitness data..."):

                url = "https://health-calculator-api.p.rapidapi.com/dcn"
                querystring = {
                    "age": age,
                    "weight": weight,
                    "height": height,
                    "gender": sex,
                    "activity_level": level_json,
                    "goal": goal_json,
                    "equation": "mifflin"
                }
                headers = {
                    "x-rapidapi-key": API_KEY,
                    "x-rapidapi-host": "health-calculator-api.p.rapidapi.com"
                }
                response = requests.get(url, headers=headers, params=querystring)

                if response.status_code == 200:
                    data = response.json()
                    if 'caloric_needs' in data and 'calories' in data['caloric_needs'] and 'goal' in data['caloric_needs']:
                        calories_str = data['caloric_needs']['calories']
                        goal_name = data['caloric_needs']['goal']

                        calories_value = float(calories_str.split()[0])

                        st.success("Daily Calorie Needs")
                        st.metric(label="Calories (kcal/day)", value=f"{calories_value:.2f} kcal")
                        st.write(f"Your current goal: **{goal_name.replace('_', ' ').title()}**")
                    else:
                        st.error("Unexpected data format from API.")
                else:
                    st.error("Failed to fetch calorie data.")

                # Advanced mode: water intake and macros
                if user == "Advanced":

                    url_dwi = "https://health-calculator-api.p.rapidapi.com/dwi"
                    querystring_dwi = {
                        "weight": weight,
                        "activity_level": level_json,
                        "climate": climate_json,
                        "unit": "liters"
                    }
                    response_dwi = requests.get(url_dwi, headers=headers, params=querystring_dwi)
                    if response_dwi.status_code == 200:
                        data_dwi = response_dwi.json()
                        water_intake = data_dwi['water_intake']
                        st.success("Daily Water Intake")
                        st.metric(label="Water Intake (liters/day)", value=f"{water_intake:.2f} L")
                    else:
                        st.error("Failed to fetch water intake data.")

                    adjusted_level = level_json
                    adjusted_goal = goal_json
                    if level_json == 'lightly_active':
                        adjusted_level = 'moderately_active'
                    elif level_json == 'extra_active':
                        adjusted_level = 'very_active'
                    if goal_json == 'weight_gain':
                        adjusted_goal = "muscle_gain"

                    url_macro = "https://health-calculator-api.p.rapidapi.com/mnd"
                    querystring_macro = {
                        "activity_level": adjusted_level,
                        "body_composition_goal": adjusted_goal,
                        "dietary_preferences": diet_json
                    }
                    response_macro = requests.get(url_macro, headers=headers, params=querystring_macro)
                    if response_macro.status_code == 200:
                        data_macro = response_macro.json()

                        carbs_percentage = data_macro['carbohydrates']
                        protein_percentage = data_macro['proteins']
                        fats_percentage = data_macro['fats']

                        carbs = (float(carbs_percentage.strip('%')) / 100) * float(calories_value) / 4
                        protein = (float(protein_percentage.strip('%')) / 100) * float(calories_value) / 4
                        fats = (float(fats_percentage.strip('%')) / 100) * float(calories_value) / 9

                        macro_df = pd.DataFrame({
                            'Nutrient': ['Carbohydrates', 'Proteins', 'Fats'],
                            'Grams': [carbs, protein, fats]
                        }).set_index('Nutrient')
                        st.dataframe(macro_df.round(2))

                        # Pie chart
                        labels = ['Carbohydrates', 'Proteins', 'Fats']
                        sizes = [carbs,protein,fats]
                        colors = ["#ff7e7e",'#66b3ff','#99ff99']

                        fig, ax = plt.subplots()
                        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
                        ax.axis('equal')
                        st.pyplot(fig)
                    else:
                        st.error("Failed to fetch macronutrient data.")

def maps(levels, goals, diets=None, climates="Average"):

    level_map = {
        "Sedentary": "sedentary",
        "Lightly Active": "lightly_active",
        "Moderately Active": "moderately_active",
        "Very Active": "very_active",
        "Extremely Active": "extra_active"
    }
    goal_map = {
        "Cut": "weight_loss",
        "Maintain": "maintenance",
        "Bulk": "weight_gain"
    }
    diet_map = {
        "Regular": None,
        "Vegetarian": "vegetarian",
        "Vegan": "vegan",
        "Gluten-Free": "gluten-free",
        "Pescatarian": "pescatarian"
    }
    climate_map = {
        "Cold": "cold",
        "Average": "normal",
        "Hot": "hot"
    }

    return level_map.get(levels), goal_map.get(goals), diet_map.get(diets), climate_map.get(climates)


if __name__ == "__main__":
    main()