from utils.constants import (
    KAFKA_TOPIC_VEHICLE_INVENTORY_DATA,
    KAFKA_TOPIC_USER_DATA,
    KAFKA_TOPIC_DRIVER_PROFILE_DATA,
    KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA,
    FLEET_INVENTORY_FILENAME,
    DRIVER_PROFILE_FILENAME,
    USER_DATA_FILENAME,
)
from generate_fake_inventory import (
    generate_fake_vehicle_inventory,
    generate_fake_driver_profile,
    generate_fake_user_data,
    generate_fake_vehicle_operational_data,
)

from random import randint
import json
import logging
import argparse

from quixstreams import Application
from pathlib import Path
from pprint import pprint
from threading import Thread

import os
import time


def get_fleet_vehicle_list(arg_dict) -> list:
    """
    Get  vehicle list
    """
    fleet_datafile_exists = False

    fleet_file_path = Path(FLEET_INVENTORY_FILENAME)

    if fleet_file_path.exists():
        logging.info("Fleet DataFile exists: %s", fleet_file_path)
        fleet_datafile_exists = True
    else:
        logging.info("Fleet DataFile doesn't exist: %s", fleet_file_path)

    fleet_vehicle_list = []

    if fleet_datafile_exists and (arg_dict.create_new in ['n', 'N']):
        with open(fleet_file_path, "r") as fleet_file:
            fleet_vehicle_list = json.load(fleet_file)
            logging.info(
                "Fleet DataFile read complete: File '%s', count %d",
                fleet_file_path,
                len(fleet_vehicle_list),
            )
    else:
        fleet_vehicle_list = generate_fake_vehicle_inventory(arg_dict.number)
        if arg_dict.create_new in ['y', 'Y']:
            logging.info("Overwriting file with new data")

        with open(fleet_file_path, "w") as fleet_file:
            json.dump(fleet_vehicle_list, fleet_file, indent=4)
            logging.info(
                "Fleet DataFile write complete: File '%s', count %d",
                fleet_file_path,
                len(fleet_vehicle_list),
            )

    # pprint(fleet_vehicle_list)
    return fleet_vehicle_list


def get_driver_profile_list(fleet_vehicle_list: list = None) -> list:
    """
    Get  Driver Profile List
    """
    driver_profile_datafile_exists = False

    driver_profile_filepath = Path(DRIVER_PROFILE_FILENAME)

    if driver_profile_filepath.exists():
        logging.info("Driver DataFile exists: %s", driver_profile_filepath)
        driver_profile_datafile_exists = True
    else:
        logging.info("Driver DataFile doesn't exist: %s", driver_profile_filepath)

    driver_data_list = []

    if driver_profile_datafile_exists:
        with open(driver_profile_filepath, "r") as driver_profile_file:
            driver_data_list = json.load(driver_profile_file)
            logging.info(
                "Driver DataFile read complete: File '%s', count %d",
                driver_profile_filepath,
                len(driver_data_list),
            )
    else:
        driver_data_list = generate_fake_driver_profile(
            driver_count=50, synthetic_fleet_data=fleet_vehicle_list
        )
        with open(driver_profile_filepath, "w") as driver_data_file:
            json.dump(driver_data_list, driver_data_file, indent=4)
            logging.info(
                "Driver DataFile write complete: File '%s', count %d",
                driver_profile_filepath,
                len(driver_data_list),
            )

    # pprint(driver_data_list)
    return driver_data_list


def get_user_data_list(fleet_vehicle_list: list = None) -> list:
    """
    Get User Data List
    """
    user_datafile_exists = False

    user_data_filepath = Path(USER_DATA_FILENAME)

    if user_data_filepath.exists():
        logging.info("User DataFile exists: %s", user_data_filepath)
        user_datafile_exists = True
    else:
        logging.info("User DataFile doesn't exist: %s", user_data_filepath)

    user_data_list = []

    if user_datafile_exists:
        with open(user_data_filepath, "r") as user_data_file:
            user_data_list = json.load(user_data_file)
            logging.info(
                "User DataFile read complete: File '%s', count %d",
                user_data_filepath,
                len(user_data_list),
            )
    else:
        user_data_list = generate_fake_user_data(
            user_count=50, synthetic_driver_data=fleet_vehicle_list
        )
        with open(user_data_filepath, "w") as user_data_file:
            json.dump(user_data_list, user_data_file, indent=4)
            logging.info(
                "User DataFile write complete: File '%s', count %d",
                user_data_filepath,
                len(user_data_list),
            )

    # pprint(user_data_list)
    return user_data_list


def vehicle_operational_data_thread(vehicle_list: list = None):
    """
    Publish Vehicle operational data to Kafka periodically
    """
    while True:
        vehicle_operational_data_list = generate_fake_vehicle_operational_data(
            fleet_data_list=vehicle_list
        )
        # pprint(vehicle_operational_data_list)
        publish_on_kafka(
            data_list=vehicle_operational_data_list,
            topic_arg=KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA,
            key_arg="vin",
        )
        time.sleep(randint(0, 10))


def publish_on_kafka(data_list: list, topic_arg: str, key_arg: str):
    """
    Publish the data on given Kafka topic
    """
    app = Application(broker_address="localhost:9092", loglevel="DEBUG")

    with app.get_producer() as producer:
        for data_obj in data_list:
            try:
                producer.produce(
                    topic=topic_arg, key=data_obj[key_arg], value=json.dumps(data_obj)
                )
                logging.info(
                    "Published for topic: %s key: %s", topic_arg, data_obj[key_arg]
                )

            except:
                logging.error(
                    "Error publishing to topic: %s key: %s",
                    topic_arg,
                    data_obj[key_arg],
                )

    return


def publish_fleet_data(fleet_list: list):
    """
    Publish fleet data on kafka
    """
    publish_on_kafka(
        data_list=fleet_list,
        topic_arg=KAFKA_TOPIC_VEHICLE_INVENTORY_DATA,
        key_arg="vin",
    )

    return


def create_and_publish_driver_profile_and_user_data(fleet_list: list):
    """
    Create and publish driver profile and user data on kafka
    """
    driver_profile_list = get_driver_profile_list(fleet_vehicle_list=fleet_list)
    publish_on_kafka(
        data_list=driver_profile_list,
        topic_arg=KAFKA_TOPIC_DRIVER_PROFILE_DATA,
        key_arg="driver_id",
    )

    user_data_list = get_user_data_list(fleet_vehicle_list=driver_profile_list)
    publish_on_kafka(
        data_list=user_data_list, topic_arg=KAFKA_TOPIC_USER_DATA, key_arg="email"
    )

    return


def create_vehicle_operational_data_thread(fleet_list: list):
    """
    Create a thread which publishes vehicle operational data periodically
    """
    vehicle_data_thread = Thread(
        target=vehicle_operational_data_thread, args=(fleet_list,)
    )
    vehicle_data_thread.daemon = True
    vehicle_data_thread.start()

    return


def main():
    logging.info("START")

    # Parse the input arguments
    arg_parser = argparse.ArgumentParser(description="Vehicle synthetic data generator program")
    arg_parser.add_argument("-n", "--number", type=int, default=2, help="Number of vehicles required")
    arg_parser.add_argument("-c", "--create-new", choices=["y", "Y", "n", "N"], default='n', help="Create new vehicle data")

    args = arg_parser.parse_args()
    #print(args)

    # Fleet Inventory, User and Driver profile creation
    fleet_vehicle_list = get_fleet_vehicle_list(args)
    # pprint(fleet_vehicle_list)
    publish_fleet_data(fleet_vehicle_list)
    create_and_publish_driver_profile_and_user_data(fleet_vehicle_list)

    # Periodic threads
    # Thread which creates Vehicle operational data
    create_vehicle_operational_data_thread(fleet_vehicle_list)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
