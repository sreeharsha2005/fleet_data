# User View Class


class User:

    user_id = ""
    first_name = ""
    last_name = ""
    email = ""
    mob_number = ""
    height_in_cm = ""
    linked_vehicle_list = []
    driver_profile_id_list = []

    def __init__(
        self,
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        mob_number: str,
        height_in_cm: int,
        linked_vehicle_list: list,
        driver_profile_id_list: list,
    ):

        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mob_number = mob_number
        self.height_in_cm = height_in_cm
        self.linked_vehicles = linked_vehicle_list
        self.driver_profile_id_list = driver_profile_id_list
