import datetime
import streamlit as st
import pandas as pd
from functions.execute_query import execute_query
from functions.read_query import read_query
import altair as alt


st.subheader("Forecasting Ad Impressions")

st.write("Using the generated data, an ML model is trained to forecast the ad-impressions. You can input the number of days you wish to forecast the ad-impressions for, and the snowflake powered ML model comes up with predictions for each of the given days.")

day = st.number_input("Enter the number of days you wish to forecast for", min_value=7, max_value=None, value=7)


actual_data = read_query(f'queries/data/data_fetch_script.sql')

forecast_model = read_query(f"queries/forecast/forecast_model_script.sql")

forecast_call = (read_query(f'queries/forecast/forecast_call_script.sql').replace("{day_param}", str(day)))

button_clicked = st.button('Execute', key=1003)
if button_clicked:
    
    execute_query(forecast_model)

    df_1 = execute_query(forecast_call, True)
    df_2 = execute_query(actual_data, True)
    print(df_1.columns)
    print(df_2.columns)
    
    df_3 = pd.DataFrame(columns=['Days','Impression_counts'])
    df_3['Days'] = pd.concat([df_1['TS'],df_2['DAY']],axis=0,ignore_index=True)
    df_3['Impression_count'] = pd.concat([df_1['FORECAST'],df_2['IMPRESSION_COUNT']],axis=0,ignore_index=True)
    
    df_3 = df_3.sort_values('Days')

    # Creating color coding column
    df_3['Legend'] = ['Actual' if i < len(df_3)-day else 'Forecast' for i in range(len(df_3))]

    
    # Creating a color-coded line chart
    chart = alt.Chart(df_3).mark_line().encode(
        x='Days',
        y='Impression_count',
        color=alt.Color('Legend', scale=alt.Scale(domain=['Actual', 'Forecast'], range=['grey', 'orange']))
    ).properties(width=600, height=400)

    st.markdown(f"Here's a graph showing the actual ad-impressions that the model has been trained for and forecasted ad-impressions")
    st.altair_chart(chart, use_container_width=True)
       
st.markdown("---")