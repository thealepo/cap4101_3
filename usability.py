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
        df_new.to_csv(csv_file , mode='a' , header=False , index=False)

def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()
    
def task_helper(task_name , task_description , timer=False):
    st.subheader(f"{task_name}")
    st.write(task_description)

    duration_val = ''
    if timer:
        if st.button("Start Task Timer"):
            st.session_state["start_time"] = time.time()
            st.info("Timer started. Complete the task and click 'Stop Task Timer'.")

        if st.button("Stop Task Timer") and "start_time" in st.session_state:
            duration_val = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration_val
            st.success(f"Task completed in {duration_val:.2f} seconds!")

    success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
    notes = st.text_area("Observer Notes")

    if st.button("Save Task Results"):
        duration_val = st.session_state.get("task_duration", "")
        data_dict = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "task_name": task_name,
            "success": success,
            "duration_seconds": duration_val,
            "notes": notes
        }
        save_to_csv(data_dict, TASK_CSV)
        st.success("Task Data Submitted!")

        if "start_time" in st.session_state:
            del st.session_state["start_time"]
        if "task_duration" in st.session_state:
            del st.session_state["task_duration"]  
    

def main():
    st.title("Usability Testing Tool")

    home , consent , demographics , tasks , exit , report = st.tabs(["Home" , "Consent" , "Demographic" , "Task" , "Exit Questionnaire" , "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the usability testing interface. Please proceed through each tab:
        1. Give consent
        2. Fill out demographics
        3. Complete tasks
        4. Submit exit questionnaire
        5. View aggregated data in the Report tab
        """)
        
    with consent:
        st.header("Consent Form")
        st.write("""
        Please read the following consent agreement carefully.
        """)
        st.write("""
        **Consent Agreement**
        - Your data will be used for research purposes only.
        - You may withdraw at any time.
        - All responses are anonymous.
        """)
        
        consent_given = st.checkbox("I agree to the terms above")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
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

            submitted = st.form_submit_button("Submitted Demographics")
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

        selected_task = st.selectbox("Select Task", ["Task 1: Full App Flow (Timed)" , "Task 2: Advanced Mode Testing" , "Task 3: Interpreting Output"])

        if selected_task == "Task 1: Full App Flow (Timed)":
            task_helper(
                task_name="Task 1",
                task_description="Time how long it takes to complete the entire app using Advanced Mode.",
                timer=True
            )
        elif selected_task == "Task 2: Enable Advanced Mode":
            task_helper(
                task_name="Task 2",
                task_description="Use Advanced Mode to display additional info and graphs."
            )
        else:
            task_helper(
                task_name="Task 3",
                task_description="Look at the calories, water intake, and macronutrient results. Report if they are understandable without help."
            )


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
