import datetime
import pandas as pd
import streamlit as st
from functions.execute_query import execute_query
from functions.read_query import read_query

# Page Configuration
st.set_page_config(layout="wide", page_title="AI-Driven Ad Insights")
st.title("Ad Impressions: Forecast & Anomaly Detection")

# The Pitch
st.markdown(
    """
    ## Smarter Ad Campaigns with ML  
    Managing ad campaign pacing can be challenging. 📉📈 A small misstep in spend allocation can impact delivery or waste budget.

    This tool leverages **Snowflake ML-powered forecasting** to help advertisers and media publishers:  
    - **Forecast future impressions** with AI-driven time series analysis.  
    - **Detect anomalies** in campaign performance early.  
    - **Optimize ad spend** by identifying gaps and reallocating resources efficiently.

    Whether you're optimizing ad spend or tracking campaign performance, this tool provides the insights you need. 🚀
    """
)

def main():
    """Main function to handle data generation and visualization."""
    st.header("Generate Sample Data")

    st.write(
        "To better understand ad campaign trends, generate sample impression data. 📊 This tool simulates real-world fluctuations, "
        "including weekday traffic spikes and weekend slowdowns. Adjust the parameters to see different scenarios."
    )

    try:
        # User inputs
        days_param = st.number_input("Number of Days", min_value=30, max_value=160, value=60)
        date_param = st.date_input(
            "Start Date", 
            value=datetime.date(2024, 1, 1),
            min_value=datetime.date(2024, 1, 1),
            max_value=datetime.date(2024, 12, 31)
        )

        if st.button("Generate Data", key=1002):
            generate_and_display_data(days_param, date_param)

    except IndexError as ie:
        st.error(f"Error: {ie}")
    except BaseException as e:
        st.error(f"Unexpected error: {e}")

    st.markdown("---")


def generate_and_display_data(days: int, start_date: datetime.date):
    """Generates ad impression data and visualizes it."""

    # Save session state
    st.session_state.date_param = start_date
    st.session_state.days_param = days

    # Read and execute SQL queries
    execute_query(read_query("queries/data/delete_script.sql"))  # Clear table
    execute_query(
        read_query("queries/data/data_generation_script.sql")
        .replace("{days_param}", str(days))
        .replace("{date_param}", start_date.strftime("%Y-%m-%d"))
    )
    execute_query(
        read_query("queries/data/trend_addition_script.sql")
        .replace("{date_param}", start_date.strftime("%Y-%m-%d"))
    )

    # Fetch generated data
    df = execute_query(read_query("queries/data/data_fetch_script.sql"), fetch_results=True)

    if df.empty:
        st.warning("No data generated. Please adjust the parameters and try again.")
        return

    # Display Data
    st.table(df)

    st.write("### Data Visualization")
    st.line_chart(data=df, x="DAY", y="IMPRESSION_COUNT", color="#FF5733")

    st.markdown(
        """
        ## Why It Matters  
        - **Proactive Anomaly Detection** – Identify issues in campaign pacing before they become costly.  
        - **Data-Driven Insights** – Make smarter budget allocation decisions based on forecasting data.  
        - **Real-Time Adjustments** – Ensure your ad spend aligns with campaign goals.

        Leverage **AI-driven forecasting and anomaly detection** to optimize your ad campaigns with confidence. 🚀
        """
    )


if __name__ == "__main__":
    main()
