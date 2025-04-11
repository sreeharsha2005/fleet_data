import logging
import time

from pprint import pprint
from uuid import uuid4

from faker import Faker
from faker_vehicle import VehicleProvider
from faker.providers import automotive
from utils.constants import VEHICLE_BRAND_RIVIAN
from random import choice, randint
from models.vehicle_view import Vehicle, VehicleOperatingData, TpmsData, CollisionAlerts

from models.user_view import User
from models.driver_profile_view import (
    DriverProfile,
    MirrorPreference,
    SteeringPreference,
    SeatPreference,
    XYSetting,
)

VEHICLE_MODELS_RIVIAN = list(VEHICLE_BRAND_RIVIAN["models"].keys())


def generate_fake_vehicle_inventory(inventory_count: int) -> list:
    faker_obj = Faker("en_US")

    faker_obj.add_provider(automotive)
    faker_obj.add_provider(VehicleProvider)
    # print(VEHICLE_MODELS_RIVIAN)

    synthetic_fleet_data = []
    for index in range(inventory_count):
        vehicle = Vehicle(
            vin=faker_obj.vin(),
            year=choice(["2021", "2025"]),
            make=VEHICLE_BRAND_RIVIAN["name"],
            model=choice(VEHICLE_MODELS_RIVIAN),
        )

        synthetic_fleet_data.append(vars(vehicle))

    # pprint(synthetic_fleet_data)
    return synthetic_fleet_data


def generate_fake_driver_profile(
    driver_count: int, synthetic_fleet_data: list = None
) -> list:
    faker_obj = Faker("en_US")

    faker_obj.add_provider(automotive)
    # faker_obj.add_provider(VehicleProvider)
    # print(VEHICLE_MODELS_RIVIAN)

    use_fleet_data = False
    if synthetic_fleet_data:
        use_fleet_data = True
        driver_count = len(synthetic_fleet_data)

    synthetic_driver_profile_data = []
    for index in range(driver_count):
        driver = DriverProfile(
            driver_id=uuid4().hex,
            user_id=uuid4().hex,
            linked_vin=[
                (
                    synthetic_fleet_data[index]["vin"]
                    if use_fleet_data
                    else faker_obj.vin()
                )
            ],
            seat_preference=vars(
                SeatPreference(
                    horizontal_setting=randint(0, 100),
                    height_setting=randint(0, 100),
                    inclination_setting=randint(80, 120),
                    lumbar_setting=randint(0, 100),
                )
            ),
            mirror_preference=vars(
                MirrorPreference(
                    left=vars(
                        XYSetting(horizontal=randint(0, 100), vertical=randint(0, 100))
                    ),
                    right=vars(
                        XYSetting(horizontal=randint(0, 100), vertical=randint(0, 100))
                    ),
                    rear_view=vars(
                        XYSetting(horizontal=randint(0, 100), vertical=randint(0, 100))
                    ),
                )
            ),
            steering_preference=vars(
                SteeringPreference(
                    vertical_setting=randint(0, 100), telescopic_setting=randint(0, 100)
                )
            ),
        )

        synthetic_driver_profile_data.append(vars(driver))

    # pprint(synthetic_driver_profile_data)
    return synthetic_driver_profile_data


def generate_fake_user_data(
    user_count: int, synthetic_driver_data: list = None
) -> list:
    faker_obj = Faker("en_US")

    faker_obj.add_provider(automotive)

    use_driver_data = False
    if synthetic_driver_data:
        use_driver_data = True
        user_count = len(synthetic_driver_data)

    synthetic_user_profile_data = []
    for index in range(user_count):
        user = User(
            user_id=uuid4().hex,
            first_name=faker_obj.first_name(),
            last_name=faker_obj.last_name(),
            email=faker_obj.email(),
            mob_number="+1-" + faker_obj.msisdn()[3:],
            height_in_cm=randint(120, 180),
            linked_vehicle_list=synthetic_driver_data[index]["linked_vin"],
            driver_profile_id_list=[synthetic_driver_data[index]["driver_id"]],
        )
        synthetic_user_profile_data.append(vars(user))

    return synthetic_user_profile_data


def generate_fake_vehicle_operational_data(fleet_data_list: list = None) -> list:
    faker_obj = Faker("en_US")

    faker_obj.add_provider(automotive)

    synthetic_fleet_operational_data = []
    for index in range(len(fleet_data_list)):
        vehicle_data = VehicleOperatingData(
            vin=fleet_data_list[index]["vin"],
            timestamp=int(time.time()),
            tire_pressure=vars(
                TpmsData(
                    tpms_fl=randint(350, 450),  # PSI*10
                    tpms_fr=randint(350, 450),  # PSI*10
                    tpms_rl=randint(350, 450),  # PSI*10
                    tpms_rr=randint(350, 450),  # PSI*10
                )
            ),
            collision_alerts=vars(
                CollisionAlerts(
                    front=(
                        int(time.time() % 100) - randint(1, 10)
                        if (int(time.time() % 100) == 25)
                        else 0
                    ),
                    right=(
                        int(time.time() % 100) - randint(30, 40)
                        if (int(time.time() % 100) == 50)
                        else 0
                    ),
                    left=(
                        int(time.time() % 100) - randint(50, 60)
                        if (int(time.time() % 100) == 75)
                        else 0
                    ),
                    back=(
                        int(time.time() % 100) - randint(70, 80)
                        if (int(time.time() % 100) == 99)
                        else 0
                    ),
                )
            ),
        )
        synthetic_fleet_operational_data.append(vars(vehicle_data))

    return synthetic_fleet_operational_data


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    # fleet_data_list = generate_fake_vehicle_inventory(2)
    # pprint(fleet_data_list)

    # driver_profile_list = generate_fake_driver_profile(5, fleet_data_list)
    # pprint(driver_profile_list)

    # user_data_list = generate_fake_user_data(5, driver_profile_list)
    # pprint(user_data_list)

    # vehicle_operational_data_list = generate_fake_vehicle_operational_data(
    #     fleet_data_list
    # )
    # pprint(vehicle_operational_data_list)
