# VPC Flow logs
AWS documentation: [Querying Amazon VPC flow logs](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html#vpc-flow-logs-partition-projection)

## Default

Create table for vpc flow logs <u>**v2 only**</u> with manual partitioning

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `vpc_flow_logs` (
  version int,
  account_id string,
  interface_id string,
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol bigint,
  packets bigint,
  bytes bigint,
  start bigint,
  `end` bigint,
  action string,
  log_status string
)
PARTITIONED BY (`date` date)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://<BUCKET_NAME>/AWSLogs/<ACCOUNT_ID>/vpcflowlogs/<REGION_CODE>/'
TBLPROPERTIES ("skip.header.line.count"="1");
```

```sql
ALTER TABLE vpc_flow_logs
ADD PARTITION (`date`='YYYY-MM-dd')
LOCATION 's3://<BUCKET_NAME>/AWSLogs/<ACCOUNT_ID>/vpcflowlogs/<REGION_CODE>/<YYYY>/<MM>/<dd>';
```

## Parquet + Hive compatible
AWS documentation: [Creating tables for flow logs in Apache Parquet format](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html#vpc-flow-logs-parquet)

You can remove `hour` partition
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs_parquet (
  version int,
  account_id string,
  interface_id string,
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol bigint,
  packets bigint,
  bytes bigint,
  start bigint,
  `end` bigint,
  action string,
  log_status string
)
PARTITIONED BY (
  `aws-account-id` string,
  `aws-service` string,
  `aws-region` string,
  `year` string, 
  `month` string, 
  `day` string,
  `hour` string
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://DOC-EXAMPLE-BUCKET/prefix/AWSLogs/'
TBLPROPERTIES (
  'EXTERNAL'='true', 
  'skip.header.line.count'='1'
)
```

## Partition projection
AWS documentation: [Creating and querying a table for Amazon VPC flow logs using partition projection](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html#vpc-flow-logs-partition-projection)

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS `vpc_flow_logs` (
  version int,
  account_id string,
  interface_id string,
  srcaddr string,
  dstaddr string,
  srcport int,
  dstport int,
  protocol bigint,
  packets bigint,
  bytes bigint,
  start bigint,
  `end` bigint,
  action string,
  log_status string
)
PARTITIONED BY (accid string, region string, day string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://<BUCKET_NAME>/'
TBLPROPERTIES
(
  "skip.header.line.count"="1",
  "projection.enabled" = "true",
  "projection.accid.type" = "enum",
  "projection.accid.values" = "111122223333,444455556666",
  "projection.region.type" = "enum",
  "projection.region.values" = "us-east-1,us-west-2",
  "projection.day.type" = "date",
  "projection.day.range" = "2024/01/01,NOW",
  "projection.day.format" = "yyyy/MM/dd",
  "storage.location.template" = "s3://<BUCKET_NAME>/AWSLogs/${accid}/vpcflowlogs/${region}/${day}"
)
```

## Dynamic ID partitioning
AWS documentation: [Dynamic ID partitioning](https://docs.aws.amazon.com/athena/latest/ug/partition-projection-dynamic-id-partitioning.html)

```sql
CREATE EXTERNAL TABLE device_events (
  event_time TIMESTAMP,
  data STRING,
  battery_level INT
)
PARTITIONED BY (
  device_id STRING
)
LOCATION "s3://DOC-EXAMPLE-BUCKET/prefix/"
TBLPROPERTIES (
  "projection.enabled" = "true",
  "projection.device_id.type" = "injected",
  "storage.location.template" = "s3://DOC-EXAMPLE-BUCKET/prefix/${device_id}"
)
```
