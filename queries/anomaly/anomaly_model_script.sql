CREATE OR REPLACE SNOWFLAKE.ML.ANOMALY_DETECTION impression_anomaly_detector(INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'daily_impressions'),
  TIMESTAMP_COLNAME => 'day',
  TARGET_COLNAME => 'impression_count',
  LABEL_COLNAME => '');