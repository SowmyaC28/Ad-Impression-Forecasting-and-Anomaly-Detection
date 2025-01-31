import streamlit as st
import pandas as pd
from functions.execute_query import execute_query
from functions.read_query import read_query


def main():
    """Main function to run the anomaly detection app."""
    st.subheader("Anomaly Detection 🔍")

    st.write(
        """
        In this section, we leverage **Snowflake-powered machine learning** to detect anomalies in ad impressions. 
        The model predicts whether the volume of impressions on a given day falls within the expected range or if it 
        is considered an anomaly that requires attention. 📊
        
        Detecting anomalies can help you identify issues like errors in campaign setup or unexpected fluctuations in ad 
        delivery, ensuring smooth and efficient operations. 
        """
    )

    try:
        # User input for impressions and date selection
        impressions = st.number_input(
            "Enter the number of impressions to be checked 📈",
            value=7000
        )

        date_param = st.date_input(
            "Select a Date 📅:",
            value=st.session_state.get("date_param", None),
            min_value=st.session_state.get("date_param", None)
        )

        if date_param is None:
            st.error("❌ Please select a valid date.")
            return

        # Read SQL queries
        anomaly_model_query = read_query("queries/anomaly/anomaly_model_script.sql")
        anomaly_call_query = read_query("queries/anomaly/anomaly_call_script.sql").replace(
            "{date_param}", date_param.strftime("%Y-%m-%d")
        ).replace("{impression}", str(impressions))

        if st.button("Check for Anomalies", key=1004):
            execute_anomaly_detection(anomaly_model_query, anomaly_call_query)

    except ValueError:
        st.error("❗ Please don't leave any fields empty.")

    st.markdown("---")


def execute_anomaly_detection(anomaly_model: str, anomaly_call: str):
    """Executes the anomaly detection queries and displays the results."""
    
    # Train the anomaly detection model
    execute_query(anomaly_model)

    # Fetch results
    result_df = execute_query(anomaly_call, fetch_results=True)

    if result_df.empty:
        st.error("❌ No data available for anomaly detection.")
        return

    # Extract anomaly result
    is_anomaly = result_df.loc[0, "IS_ANOMALY"]

    # Display result
    if is_anomaly:
        st.write("🔴 **Anomaly Detected!** The impressions for the selected date are **outside the expected range**.")
    else:
        st.write("🟢 **No Anomaly!** The impressions for the selected date are **within the expected range**.")


if __name__ == "__main__":
    main()
