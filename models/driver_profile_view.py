# Driver Profile View Class


class SeatPreference:

    horizontal_setting = 0
    height_setting = 0
    inclination_setting = 0
    lumbar_setting = 0

    def __init__(
        self,
        horizontal_setting: int,
        height_setting: int,
        inclination_setting: int,
        lumbar_setting: int,
    ):

        self.horizontal_setting = horizontal_setting
        self.height_setting = height_setting
        self.inclination_setting = inclination_setting
        self.lumbar_setting = lumbar_setting


class SteeringPreference:

    vertical_setting = 0
    telescopic_setting = 0

    def __init__(self, vertical_setting: int, telescopic_setting: int):

        self.vertical_setting = vertical_setting
        self.telescopic_setting = telescopic_setting


class XYSetting:
    horizontal = 0
    vertical = 0

    def __init__(self, horizontal: int, vertical: int):

        self.horizontal = horizontal
        self.vertical = vertical


class MirrorPreference:

    def __init__(self, left: dict, right: dict, rear_view: dict):

        self.left = left
        self.right = right
        self.rear_view = rear_view


class DriverProfile:

    driver_id = ""
    user_id = ""
    linked_vin = ""
    seat_preference = {}
    mirror_preference = {}
    steering_preference = {}

    def __init__(
        self,
        driver_id: str,
        user_id: str,
        linked_vin: str,
        seat_preference: dict,
        mirror_preference: dict,
        steering_preference: dict,
    ):

        self.driver_id = driver_id
        self.user_id = user_id
        self.linked_vin = linked_vin
        self.seat_preference = seat_preference
        self.steering_preference = steering_preference
        self.mirror_preference = mirror_preference
