import streamlit as st
import pandas as pd
import altair as alt
from functions.execute_query import execute_query
from functions.read_query import read_query


def main():
    """Main function to run the Streamlit forecasting app."""
    st.subheader("Forecasting Ad Impressions 📊")

    st.write(
        """
        With the data generated, we are now ready to forecast the **ad impressions** using machine learning models. 
        This tool provides an intuitive interface for forecasting, so you can plan ahead for your campaigns. 
        You can select the number of days you want to forecast, and the **Snowflake-powered ML model** will predict 
        the ad impressions for those days. 🔮
        
        This capability helps you make informed decisions, optimize your ad spend, and adjust your campaigns 
        before any issues arise. 🔧📈
        """
    )

    # User input for forecasting days
    day = st.number_input(
        "Enter the number of days you wish to forecast for ⏳",
        min_value=7,
        value=7
    )

    # Read SQL queries
    actual_data_query = read_query("queries/data/data_fetch_script.sql")
    forecast_model_query = read_query("queries/forecast/forecast_model_script.sql")
    forecast_call_query = read_query("queries/forecast/forecast_call_script.sql").replace(
        "{day_param}", str(day)
    )

    if st.button("Execute 🔮", key=1003):
        execute_forecasting(forecast_model_query, forecast_call_query, actual_data_query, day)


def execute_forecasting(forecast_model: str, forecast_call: str, actual_data: str, day: int):
    """Executes the forecasting queries and visualizes the results."""
    
    # Train the forecasting model
    execute_query(forecast_model)

    # Fetch forecasted and actual data
    forecast_df = execute_query(forecast_call, fetch_results=True)
    actual_df = execute_query(actual_data, fetch_results=True)

    if forecast_df.empty or actual_df.empty:
        st.error("❌ No data available for visualization. Please ensure your data is properly generated.")
        return

    # Combine datasets
    df_combined = pd.DataFrame(columns=["Days", "Impression_count"])
    df_combined["Days"] = pd.concat([forecast_df["TS"], actual_df["DAY"]], ignore_index=True)
    df_combined["Impression_count"] = pd.concat([forecast_df["FORECAST"], actual_df["IMPRESSION_COUNT"]], ignore_index=True)
    df_combined.sort_values("Days", inplace=True)

    # Assign labels for actual vs forecasted data
    df_combined["Legend"] = ["Actual" if i < len(df_combined) - day else "Forecast" for i in range(len(df_combined))]

    # Create visualization
    plot_forecast(df_combined)


def plot_forecast(df: pd.DataFrame):
    """Generates and displays a color-coded line chart for forecasting results."""
    
    chart = alt.Chart(df).mark_line().encode(
        x="Days:T",
        y="Impression_count:Q",
        color=alt.Color("Legend:N", scale=alt.Scale(domain=["Actual", "Forecast"], range=["grey", "orange"]))
    ).properties(width=600, height=400)

    st.markdown(
        """
        Here's a graph showing the **actual ad impressions** that the model has been trained on, 
        along with the **forecasted impressions** for the coming days. 📉📈

        This visualization provides a clear comparison between the past performance of your ad campaigns 
        and the model’s predictions, helping you evaluate how accurate the forecast is.
        """
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown(
        """
        ## Key Takeaways:  
        - **Actionable Insights:** Forecast future ad impressions and optimize your campaigns effectively.  
        - **Forecast Accuracy:** Compare actual vs forecasted impressions and monitor forecast performance.  
        - **Adjust in Real-Time:** Adjust your strategy based on the insights, optimizing ad spend and preventing issues.  
        
        Leverage machine learning to ensure your campaigns are performing as expected and make informed decisions. 🚀
        """
    )


if __name__ == "__main__":
    main()
