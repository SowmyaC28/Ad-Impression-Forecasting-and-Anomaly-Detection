  CALL impression_anomaly_detector!DETECT_ANOMALIES(INPUT_DATA => SYSTEM$QUERY_REFERENCE('select \'{date_param}\'::timestamp as day, {impression} as impressions'),
  TIMESTAMP_COLNAME =>'day',
  TARGET_COLNAME => 'impressions');