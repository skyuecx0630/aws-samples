from datetime import datetime, timedelta
from time import sleep
from uuid import uuid4
import json

import boto3


DELIVERY_STREAM_NAME = "iot-stream"

client = boto3.client("firehose")

# device_ids = [str(uuid4()) for _ in range(5)]
device_ids = [
    "bb699318-87f3-46b0-86c0-fef43218b25a",
    "10cd0e99-1020-4cc0-8b56-2c32059ac94e",
    "9634b374-213c-49eb-9f13-6957b2478f09",
    "d9d29655-8a67-4d9e-9a6c-838757026731",
    "3427750a-4279-4bda-b77e-ff67032dc996",
]
print(device_ids)


def put_record(record):
    response = client.put_record(
        DeliveryStreamName=DELIVERY_STREAM_NAME, Record={"Data": record}
    )
    return response


pattern = list(range(10, 22)) + list(range(22, 10, -1))

i = 0
now = datetime.now()
while True:
    record = {
        "type": "thermometer",
        "device_id": device_ids[i % len(device_ids)],
        "temperature": pattern[i % len(pattern)],
        "timestamp": now.isoformat(timespec="seconds"),
    }

    try:
        put_record(json.dumps(record))
        print(f"{datetime.now()} {record}")
    except Exception as e:
        print(e)

    sleep(1)
    now += timedelta(minutes=2)
    i += 1
