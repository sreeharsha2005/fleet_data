# Vehicle View Class


class Vehicle:

    vin = ""
    year = ""
    make = ""
    model = ""

    def __init__(self, vin: str, year: str, make: str, model: str):

        self.vin = vin
        self.year = year
        self.make = make
        self.model = model


class VehicleOperatingData:

    vin = ""
    timestamp = ""
    tire_pressure = {}
    collision_alerts = {}

    def __init__(
        self,
        vin: str,
        timestamp: int,
        tire_pressure: dict,
        collision_alerts=dict,
    ):

        self.vin = vin
        self.timestamp = timestamp
        self.tire_pressure = tire_pressure
        self.collision_alerts = collision_alerts


class TpmsData:

    tpms_fl = ""
    tpms_fr = ""
    tpms_rl = ""
    tpms_rr = ""

    def __init__(self, tpms_fl: str, tpms_fr: str, tpms_rl: str, tpms_rr: str):

        self.tpms_fl = tpms_fl
        self.tpms_fr = tpms_fr
        self.tpms_rl = tpms_rl
        self.tpms_rr = tpms_rr


class CollisionAlerts:

    front = 0
    right = 0
    left = 0
    back = 0

    def __init__(self, front: int, right: int, left: int, back: int):

        self.front = front
        self.right = right
        self.left = left
        self.back = back
