import snowflake.connector
import streamlit as st
import pandas as pd

def execute_query(query: str, fetch_results: bool = False):
    """
    Executes a query in Snowflake.

    Args:
        query (str): The SQL query to execute.
        fetch_results (bool): Whether to fetch and return query results.

    Returns:
        pd.DataFrame | None: DataFrame if fetch_results is True, else None.
    """
    try:
        # Establish connection to Snowflake
        conn = snowflake.connector.connect(
            user=st.secrets["user"],
            password=st.secrets["password"],
            account=st.secrets["account_identifier"],
            database=st.secrets["database"],
            warehouse=st.secrets["warehouse"],
            schema=st.secrets["schema"],
        )

        with conn.cursor() as cursor:
            cursor.execute(query)
            
            if fetch_results:
                result = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(result, columns=columns)

    except snowflake.connector.errors.DatabaseError as e:
        st.error(f"Database error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    finally:
        conn.close()
