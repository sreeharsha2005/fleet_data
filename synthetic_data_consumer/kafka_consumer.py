import json
import logging
import requests
import base64

from quixstreams import Application
from utils.constants import (
    KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA,
    KAFKA_CONSUMER_POLL_TIMEOUT,
    KAFKA_TOPIC_VEHICLE_INVENTORY_DATA,
    FLEET_DATA_ENDPOINT,
)


def main():
    logging.info("START")
    app = Application(
        broker_address="localhost:9092", loglevel="DEBUG", auto_offset_reset="latest"
    )

    with app.get_consumer() as kafka_consumer:
        kafka_consumer.subscribe([KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA])

        while True:
            kafka_msg = kafka_consumer.poll(KAFKA_CONSUMER_POLL_TIMEOUT)

            if kafka_msg is not None:
                logging.info(
                    "Topic: %s, Key: %s, Value:%s",
                    kafka_msg.topic(),
                    kafka_msg.key().decode("utf-8"),
                    json.loads(kafka_msg.value()),
                )

                payload = json.loads(kafka_msg.value())

                # Encoded vin
                encoded_vin = base64.b64encode(payload["vin"].encode("utf-8"))
                payload["vin"] = str(encoded_vin.decode("utf-8"))

                # Call fleet API
                #requests.post(FLEET_DATA_ENDPOINT, json=payload)

if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
