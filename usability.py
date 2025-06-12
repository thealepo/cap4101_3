import streamlit as st
import pandas as pd
import time
import os

DATA_FOLDER = 'data'
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

CONSENT_CSV = os.path.join(DATA_FOLDER , 'consent_data.csv')
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER , 'demographic_data.csv')
TASK_CSV = os.path.join(DATA_FOLDER , 'task_data.csv')
EXIT_CSV = os.path.join(DATA_FOLDER , 'exit_data.csv')

def save_to_csv(data_dict , csv_file):
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        df_new.to_csv(csv_file , mode='w' , header=True , index=False)
    else:
        df_new.to_csv(csv_file , mode='a' , header=True , index=False)

def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()
    

def main():
    st.title("Usability Testing Tool")

    home , consent , demographics , tasks , exit , report = st.tabs(["Home" , "Consent" , "Demographic" , "Task" , "Exit Questionnaire" , "Report"])

    with home:
        st.header("Introduction")
        st.write("""
                ...
                """)
        
    with consent:
        st.header("Consent Form")
        st.write("""
                 Please read consent form
                 """)
        st.write("""
                 **Consent Agreement**
                 - yada
                 - yada
                 - yada
                 """)
        
        consent_given = st.checkbox("I agree to the terms above")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree before proceeding")
            else:
                st.success("Consent Submitted!")
                data_dict = {
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'consent_given': consent_given
                }
                save_to_csv(data_dict=data_dict , csv_file=CONSENT_CSV)
        
    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):

            name = st.text_input("Name (optional)")
            age = st.text_input("Age")
            occupation = st.text_input("Occupation")
            familiarity = st.selectbox("Familiarity with tools?" , ["Not Familiar" , "Somewhat Familiar" , "Very Familiar"])

            submitted = st.form_submit_button("Submited Demographics")
            if submitted:
                st.success("Demographic Data Submitted!")
                data_dict = {
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'name': name,
                    'age': age,
                    'occupation': occupation,
                    'familiarity': familiarity
                }
                save_to_csv(data_dict=data_dict , csv_file=DEMOGRAPHIC_CSV)

    with tasks:
        st.header("Task Page")

        st.write("Please select a task and record your experience completing it")

        selected_task = st.selectbox("Select Task", ["Task 1" , "Task 2" , "Task 3"])

        if selected_task == "Task 1":
            st.write("Task Description: Time how long it takes to complete full app in Advanced Mode")

            start_button = st.button("Start TaskTimer")
            if start_button:
                st.session_state["start_time"] = time.time()
                st.info("Task timer started. Complete your task and click 'Stop Task Timer'")

            stop_button = st.button("Stop Task Timer")
            if stop_button and "start_time" in st.session_state:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
                st.success(f"Task completed in {duration:.2f} seconds!")

            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
            notes = st.text_area("Observer Notes")

            if st.button("Save Task Results"):
                duration_val = st.session_state.get("task_duration", None)
                st.success("Task Data Submitted!")

                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "notes": notes
                }
                save_to_csv(data_dict, TASK_CSV)
                
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]

        elif selected_task == "Task 2":
            st.write("Use advanced mode to display additional information + graphs")
            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
            notes = st.text_area("Observer Notes")
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)

        else:
            st.write("After submitting, look at the calories and macronutrient results, and report if you can understand what they mean or if you need help tags")
            success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
            notes = st.text_area("Observer Notes")
            data_dict = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "task_name": selected_task,
                "success": success,
                "notes": notes
            }
            save_to_csv(data_dict, TASK_CSV)

    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):

            satisfaction = st.slider("Overall Satisfaction (1=Very Low, 5=Very High)" , min_value=1 , max_value=5 , value=3)
            difficulty = st.slider("Overall Difficulty (1=Very Low, 5=Very High)" , min_value=1 , max_value=5 , value=3)
            open_feedback = st.text_area("Additional feedback or comments")

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                st.success("Exit Questionnaire Data Saved.")
                data_dict = {
                    'timestamp': time.strftime("%Y-%m-%d $H:%M:%S"),
                    'satisfaction': satisfaction,
                    'difficulty': difficulty,
                    'open_feedback': open_feedback
                }
                save_to_csv(data_dict=data_dict , csv_file=EXIT_CSV)
                

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        if not exit_df.empty:
            st.subheader("Exit Questionnaire Averages")
            avg_satisfaction = exit_df['satisfaction'].mean()
            avg_difficulty = exit_df['difficulty'].mean()
            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")


if __name__ == "__main__":
    main()
        

                

