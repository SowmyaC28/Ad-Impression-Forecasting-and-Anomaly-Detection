CREATE OR REPLACE SNOWFLAKE.ML.FORECAST impressions_forecast(INPUT_DATA =>
    SYSTEM$REFERENCE('TABLE', 'daily_impressions'),
                    TIMESTAMP_COLNAME => 'day',
                    TARGET_COLNAME => 'impression_count'
    );