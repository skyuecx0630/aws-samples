# Redshift ML

```sql
CREATE MODEL predict_web_attacks
FROM (
    select dst_port,
        protocol,
        flow_duration,
        tot_fwd_pkts,
        tot_bwd_pkts,
        totlen_fwd_pkts,
        totlen_bwd_pkts,
        tot_fwd_pkt_len_max,
        tot_fwd_pkt_len_min,
        tot_fwd_pkt_len_mean,
        tot_fwd_pkt_len_std_dev,
        tot_bwd_pkt_len_max,
        tot_bwd_pkt_len_min,
        tot_bwd_pkt_len_mean,
        tot_bwd_pkt_len_std_dev,
        flow_bytes,
        flow_pkts,
        flow_iat_mean,
        flow_iat_std_dev,
        flow_iat_max,
        flow_iat_min,
        fwd_iat_tot,
        fwd_iat_mean,
        fwd_iat_std_dev,
        fwd_iat_max,
        fwd_iat_min,
        bwd_iat_tot,
        bwd_iat_mean,
        bwd_iat_std_dev,
        bwd_iat_max,
        bwd_iat_min,
        label
    FROM network_logs
)
TARGET label
FUNCTION predict_web_attacks
IAM_ROLE 'arn:aws:iam::856210586235:role/redshift-query-role'
AUTO OFF
MODEL_TYPE XGBOOST
OBJECTIVE 'multi:softmax'
PREPROCESSORS 'none'
HYPERPARAMETERS DEFAULT EXCEPT (NUM_CLASS '5')
SETTINGS (
    S3_BUCKET 'BUCKET_NAME',
    MAX_RUNTIME 1500
);
```

## Debug
On Redshift Serverless, some system tables(including STV_ML_MODEL_INFO) are [not accessible](https://repost.aws/questions/QUr1ywNL6kQPOglpmRVMCtCA/redshift-superuser-permission-denied-to-stl-tables). 
```sql
select schema_name, model_name, model_state from stv_ml_model_info;
```
```sql
SHOW MODEL ALL;
```
```sql
SHOW MODEL predict_web_attacks;
```