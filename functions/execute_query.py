import snowflake.connector
import streamlit as st
import pandas as pd

def execute_query(query, fetch_results=False):
    # Establish connection to Snowflake
    conn = snowflake.connector.connect(
        user=st.secrets.user,
        password=st.secrets.password,
        account=st.secrets.account_identifier,
        database=st.secrets.database,
        warehouse=st.secrets.warehouse,
        schema=st.secrets.schema,
    )

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        if fetch_results:
            # Fetch the results
            result = cursor.fetchall()
            
            # Fetch column names
            columns = [desc[0] for desc in cursor.description]
            
            # Create a DataFrame
            df = pd.DataFrame(result, columns=columns)
            
            return df
    finally:
        cursor.close()
        conn.close()
