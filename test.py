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