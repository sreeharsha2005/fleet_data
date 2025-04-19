import json
import logging
import requests
import base64
from threading import Thread
import time
from pprint import pprint


from quixstreams import Application
from utils.constants import (
    KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA,
    KAFKA_CONSUMER_POLL_TIMEOUT,
    KAFKA_TOPIC_VEHICLE_INVENTORY_DATA,
    KAFKA_TOPIC_DRIVER_PROFILE_DATA,
    KAFKA_TOPIC_USER_DATA,
    FLEET_VEHICLE_DATA_ENDPOINT,
    FLEET_OPERATING_DATA_ENDPOINT,
)


def call_vehicle_inventory_data_api(kafka_message):
    """
    Call Vehicle inventory POST API to store the vehicle data
    """
    payload = json.loads(kafka_message.value())
    # Encoded vin
    encoded_vin = base64.b64encode(payload["vin"].encode("utf-8"))
    payload["vin"] = str(encoded_vin.decode("utf-8"))

    # Call fleet API
    requests.post(FLEET_VEHICLE_DATA_ENDPOINT, json=payload)


def call_vehicle_operational_data_api(kafka_message):
    """
    Call Vehicle Operating Data POST API to store vehicle operating info
    """
    payload = json.loads(kafka_message.value())
    # Encoded vin
    encoded_vin = base64.b64encode(payload["vin"].encode("utf-8"))
    payload["vin"] = str(encoded_vin.decode("utf-8"))

    # Call fleet Operating Data API
    resp = requests.post(FLEET_OPERATING_DATA_ENDPOINT, json=payload)
    # pprint(payload)
    # print(resp.content)


def fleet_data_consumer_thread():
    """
    Consume kafka message and call REST APIs by topic
    """
    kafka_app = Application(
        broker_address="localhost:9092", loglevel="DEBUG", auto_offset_reset="latest"
    )
    with kafka_app.get_consumer() as kafka_consumer:
        kafka_consumer.subscribe(
            [
                KAFKA_TOPIC_VEHICLE_INVENTORY_DATA,
                KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA,
                # KAFKA_TOPIC_DRIVER_PROFILE_DATA,
                # KAFKA_TOPIC_USER_DATA,
            ]
        )

        while True:
            kafka_msg = kafka_consumer.poll(KAFKA_CONSUMER_POLL_TIMEOUT)

            if kafka_msg is None:
                logging.info("waiting...")
            elif kafka_msg.error() is not None:
                logging.error("error - ", kafka_msg.error())
            else:
                logging.info(
                    "Topic: %s, Key: %s, Value:%s",
                    kafka_msg.topic(),
                    kafka_msg.key().decode("utf-8"),
                    json.loads(kafka_msg.value()),
                )

                if kafka_msg.topic() == KAFKA_TOPIC_VEHICLE_INVENTORY_DATA:
                    call_vehicle_inventory_data_api(kafka_msg)
                elif kafka_msg.topic() == KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA:
                    call_vehicle_operational_data_api(kafka_msg)
                # elif kafka_msg.topic() == KAFKA_TOPIC_DRIVER_PROFILE_DATA:
                #     call_driver_profile_data_api(kafka_msg)
                # elif kafka_msg.topic() == KAFKA_TOPIC_USER_DATA:
                #     call_user_data_api(kafka_msg)

                else:
                    logging.error(
                        "Topic: %s - Message Handler unavailable", kafka_msg.topic()
                    )


def start_fleet_data_consumer_thread():
    """
    Create a thread which consumes fleet data periodically
    """
    vehicle_data_consumer_thread = Thread(target=fleet_data_consumer_thread)
    vehicle_data_consumer_thread.daemon = True
    vehicle_data_consumer_thread.start()

    return


def main():
    """
    Invoke the fleet data consumer thread
    """
    logging.info("START")
    start_fleet_data_consumer_thread()

    while True:
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
