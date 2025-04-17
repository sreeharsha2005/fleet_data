# Constant values to be used during synthetic data preparation

import os

VEHICLE_BRAND_RIVIAN = {
    "name": "Rivian",
    "established": 2009,
    "models": {
        "R1T": "Truck",
        "R1S": "SUV",
        "R2": "SUV",
        "R3": "SUV/Crossover",
        "V": "Delivery Vans",
    },
}

KAFKA_TOPIC_VEHICLE_INVENTORY_DATA = "vehicle_inventory_data"
KAFKA_TOPIC_VEHICLE_OPERATIONAL_DATA = "vehicle_oper_data"
KAFKA_TOPIC_DRIVER_PROFILE_DATA = "driver_profile_data"
KAFKA_TOPIC_USER_DATA = "user_data"
KAFKA_CONSUMER_POLL_TIMEOUT = 3 # 3 seconds

#Base directory path
BASE_DIR = os.path.dirname(os.getcwd())

#Fleet data storage filenames
STATIC_DATA_STORE_DIR = "static_data_store"
FLEET_INVENTORY_FILENAME = BASE_DIR + "/" + STATIC_DATA_STORE_DIR + "/" + "vin_data.json"
DRIVER_PROFILE_FILENAME = BASE_DIR + "/" + STATIC_DATA_STORE_DIR + "/" + "driver_profile_data.json"
USER_DATA_FILENAME = BASE_DIR + "/" + STATIC_DATA_STORE_DIR + "/" + "user_data.json"

# DRF API endpoints
FLEET_DATA_ENDPOINT = "http://localhost:8010/api/v1/vehicles/"
FLEET_OPERATING_DATA_ENDPOINT = "http://localhost:8010/api/v1/vehicles/operatingdata/"
