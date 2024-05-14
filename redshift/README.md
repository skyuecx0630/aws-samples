# Redshift

## Spectrum
AWS documentation: [Getting started with Amazon Redshift Spectrum](https://docs.aws.amazon.com/redshift/latest/dg/c-getting-started-using-spectrum.html)

IAM permisson `AWSGlueConsoleFullAccess` required to create external database

Or here's [minimum permissions](https://docs.aws.amazon.com/redshift/latest/dg/c-spectrum-iam-policies.html#spectrum-iam-policies-minimum-permissions)
```sql
create external schema spectrum
from data catalog
database 'spectrum'
iam_role 'arn:aws:iam::856210586235:role/redshift-query-role'
create external database if not exists;
```

There are a few differences between normal Redshift and Spectrum queries
- NO encode
- NO specific filename
```sql
CREATE EXTERNAL TABLE spectrum.network_logs
(
    dst_port bigint,
    protocol bigint,
    flow_duration bigint,
    tot_fwd_pkts bigint,
    tot_bwd_pkts bigint,
    totlen_fwd_pkts bigint,
    totlen_bwd_pkts bigint,
    tot_fwd_pkt_len_max bigint,
    tot_fwd_pkt_len_min bigint,
    tot_fwd_pkt_len_mean double precision,
    tot_fwd_pkt_len_std_dev double precision,
    tot_bwd_pkt_len_max bigint,
    tot_bwd_pkt_len_min bigint,
    tot_bwd_pkt_len_mean double precision,
    tot_bwd_pkt_len_std_dev double precision,
    flow_bytes double precision,
    flow_pkts double precision,
    flow_iat_mean double precision,
    flow_iat_std_dev double precision,
    flow_iat_max bigint,
    flow_iat_min bigint,
    fwd_iat_tot bigint,
    fwd_iat_mean double precision,
    fwd_iat_std_dev double precision,
    fwd_iat_max bigint,
    fwd_iat_min bigint,
    bwd_iat_tot bigint,
    bwd_iat_mean double precision,
    bwd_iat_std_dev double precision,
    bwd_iat_max bigint,
    bwd_iat_min bigint,
    label smallint,
    label_desc varchar(100)
)
-- ROW FORMAT DELIMITED
-- fields terminated by ','
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://redshift-demos/redshiftml-reinvent/2022/'
table properties (
    'skip.header.line.count' = '1'
);
```
```sql
select * from spectrum.network_logs limit 100;
```

## Create and load data from s3
AWS documentation: [COPY parameter reference](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY-parameters.html) /  [COPY examples](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY_command_examples.html)

```sql
create table network_logs (
    dst_port bigint ENCODE az64,
    protocol bigint ENCODE az64,
    flow_duration bigint ENCODE az64,
    tot_fwd_pkts bigint ENCODE az64,
    tot_bwd_pkts bigint ENCODE az64,
    totlen_fwd_pkts bigint ENCODE az64,
    totlen_bwd_pkts bigint ENCODE az64,
    tot_fwd_pkt_len_max bigint ENCODE az64,
    tot_fwd_pkt_len_min bigint ENCODE az64,
    tot_fwd_pkt_len_mean double precision ENCODE raw,
    tot_fwd_pkt_len_std_dev double precision ENCODE raw,
    tot_bwd_pkt_len_max bigint ENCODE az64,
    tot_bwd_pkt_len_min bigint ENCODE az64,
    tot_bwd_pkt_len_mean double precision ENCODE raw,
    tot_bwd_pkt_len_std_dev double precision ENCODE raw,
    flow_bytes double precision ENCODE raw,
    flow_pkts double precision ENCODE raw,
    flow_iat_mean double precision ENCODE raw,
    flow_iat_std_dev double precision ENCODE raw,
    flow_iat_max bigint ENCODE az64,
    flow_iat_min bigint ENCODE az64,
    fwd_iat_tot bigint ENCODE az64,
    fwd_iat_mean double precision ENCODE raw,
    fwd_iat_std_dev double precision ENCODE raw,
    fwd_iat_max bigint ENCODE az64,
    fwd_iat_min bigint ENCODE az64,
    bwd_iat_tot bigint ENCODE az64,
    bwd_iat_mean double precision ENCODE raw,
    bwd_iat_std_dev double precision ENCODE raw,
    bwd_iat_max bigint ENCODE az64,
    bwd_iat_min bigint ENCODE az64,
    label smallint ENCODE az64,
    label_desc varchar(100)
);
```

```sql
COPY network_logs
FROM 's3://redshift-demos/redshiftml-reinvent/2022/network_logs.csv'
CSV DELIMITER ','
IAM_ROLE 'arn:aws:iam::856210586235:role/redshift-query-role'
IGNOREHEADER 1;
```

## Debug
AWS documenation: [SYS_LOAD_ERROR_DETAIL](https://docs.aws.amazon.com/redshift/latest/dg/SYS_LOAD_ERROR_DETAIL.html)
```sql
SELECT * FROM sys_load_error_detail;
```
```sql
SELECT * FROM sys_load_history;
```