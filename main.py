import pandas as pd
import streamlit as st
import datetime
from functions.execute_query import execute_query
from functions.read_query import read_query



# page headings
st.set_page_config(layout="wide", page_title="snowflake ml forecast and anomaly detector")
st.title("ad impression predictor")



# with open("home_page_content.html", mode="r",  encoding="utf8") as file:
#     home_page_content = file.read()

# st.markdown(home_page_content, unsafe_allow_html=True)


# ---------------------------------------------------------------
st.header("Generate Data")

st.write("To generate data for an interesting forecasting perspective and test for yourself, you can enter the date and number of days for which you want to generate data. With these inputs, a random volume of impressions is generated for each of the given number of days ahead of the input date. To make things more interesting, data is tweaked to showcase upward and downward trends on weekdays and weekends respectively.")

    
try:

    # Parameter for number of days of data to be generated  
    days_param = st.number_input("Enter number of Days", min_value=30, max_value=160, value=60)

    # Parameter for choosing the start date for data to be generated
    date_param = st.date_input("Select Start Date:", value=datetime.date(2024, 1, 1),
                                min_value=datetime.date(2024, 1, 1),
                                max_value=datetime.date(2024, 12, 31))
   
    
    # Clean any previous data in the table
    empty_table = read_query(f"queries/data/delete_script.sql")

    # Generate the data using the parameters
    generate_data = (read_query(f"queries/data/data_generation_script.sql").replace("{days_param}", str(days_param)).replace("{date_param}", date_param.strftime("%Y-%m-%d")))
    
    # Massage the data to create some seasonality
    massage_data = read_query(f"queries/data/trend_addition_script.sql").replace("{date_param}", date_param.strftime("%Y-%m-%d"))
    
    # Fetch all the data
    fetch_all_data = read_query(f"queries/data/data_fetch_script.sql")

    button_clicked = st.button('Generate', key=1002)
   
    if button_clicked:
        
        st.session_state.date_param = date_param
        st.session_state.days_param = days_param
        
        execute_query(empty_table) # Empty table
        execute_query(generate_data) # Generate data
        execute_query(massage_data) # Massage the data
        
        
        
        df_1 = execute_query(fetch_all_data,True) # Get all the data
        print(type(df_1))

        st.table(df_1)

        st.write("Here's a graph showing the data that has been generated:")
        st.line_chart(data=df_1, x="DAY", y="IMPRESSION_COUNT", color="#0000ff") # Line chart for impressions

    st.markdown("---")

except IndexError as ie:
    st.markdown(f">:red[Please select required number of options to generate a query. Error: {ie} :fearful:]",
                unsafe_allow_html=True)
except BaseException as e:
    st.markdown(f">{e}")
    
