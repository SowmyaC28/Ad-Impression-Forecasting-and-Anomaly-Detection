import datetime
import streamlit as st
import pandas as pd
from functions.execute_query import execute_query
from functions.read_query import read_query



st.subheader("Anamoly Detection")

st.write("Using the generated data, a new Snowflake-ML model is trained to detect an anomaly. This model is now ready to predict whether the volume of ad impressions on a given day is anticipated or is an anomaly. ")

try:


    impressions = st.number_input("Enter the number of impressions to be checked", min_value=None, max_value=None, value=7000)
    date_param = st.date_input("Select a Date:", value = st.session_state.date_param,
                                    min_value = st.session_state.date_param,
                                    max_value = None)


    anomaly_model = read_query(f'queries/anomaly/anomaly_model_script.sql')
    anomaly_call = read_query(f'queries/anomaly/anomaly_call_script.sql').replace("{date_param}", date_param.strftime("%Y-%m-%d")).replace("{impression}", str(impressions))


    button_clicked = st.button('Execute',key=1004)
    if button_clicked:
        
        execute_query(anomaly_model)
        
        
        df_1 = execute_query(anomaly_call, True)
        
        ans = df_1['IS_ANOMALY'].loc[0]
        
        
        if ans is True:
            st.write("The impressions for the chosen date are an anomaly")
            
        else:
            st.write("For the chosen date the number of impressions are not an anomaly")   
    st.markdown("---")

except ValueError as e:
    st.error("Please dont leave any fields empty")