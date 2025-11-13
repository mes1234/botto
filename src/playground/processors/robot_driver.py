from dataclasses import asdict, dataclass
import json
import math
import paho.mqtt.client as mqtt
from time import sleep
from typing import Dict
from src.playground.msg.messages import (
    SensorDataMsg,
    LegAnglesPhaseMsg,
    LegEnum,
    LegAnglesMsg,
)
from src.base.process import BottoProcess


@dataclass
class ServoPositionTarget:
    # FL alfa1
    position_0: float = 90.0
    # FL alfa2
    position_1: float = 90.0
    # FL alfa3
    position_2: float = 90.0

    # ----------------
    # FR alfa1
    position_3: float = 90.0
    # FR alfa2
    position_4: float = 90.0
    # FR alfa3
    position_5: float = 90.0

    # ---------------
    # RL alfa1
    position_6: float = 90.0
    # RL alfa2
    position_7: float = 90.0
    # RL alfa3
    position_8: float = 90.0

    # ---------------
    # RR alfa1
    position_9: float = 90.0
    # RR alfa2
    position_10: float = 90.0
    # RR alfa3
    position_11: float = 90.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def map(cls, msg: Dict[LegEnum, LegAnglesMsg]) -> "ServoPositionTarget":
        servo_position_target = cls()

        # FRONT_LEFT
        servo_position_target.position_0 = msg[LegEnum.FRONT_LEFT].alfa_1
        servo_position_target.position_1 = msg[LegEnum.FRONT_LEFT].alfa_2
        servo_position_target.position_2 = msg[LegEnum.FRONT_LEFT].alfa_3

        # FRONT_RIGHT
        servo_position_target.position_3 = msg[LegEnum.FRONT_RIGHT].alfa_1
        servo_position_target.position_4 = msg[LegEnum.FRONT_RIGHT].alfa_2
        servo_position_target.position_5 = msg[LegEnum.FRONT_RIGHT].alfa_3

        # BACK_LEFT
        servo_position_target.position_6 = msg[LegEnum.BACK_LEFT].alfa_1
        servo_position_target.position_7 = msg[LegEnum.BACK_LEFT].alfa_2
        servo_position_target.position_8 = msg[LegEnum.BACK_LEFT].alfa_3

        # BACK_RIGHT
        servo_position_target.position_9 = msg[LegEnum.BACK_RIGHT].alfa_1
        servo_position_target.position_10 = msg[LegEnum.BACK_RIGHT].alfa_2
        servo_position_target.position_11 = msg[LegEnum.BACK_RIGHT].alfa_3

        return servo_position_target


class RobotDriver(BottoProcess[SensorDataMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corrections = {
            LegEnum.FRONT_LEFT: {
                "alfa_1": {"offset": 90.0, "mult": 1.0},
                "alfa_2": {"offset": 90.0, "mult": 1.0},
                "alfa_3": {"offset": 90.0, "mult": -1.0},
            },
            LegEnum.FRONT_RIGHT: {
                "alfa_1": {"offset": 90.0, "mult": 1.0},
                "alfa_2": {"offset": 90.0, "mult": -1.0},
                "alfa_3": {"offset": 90.0, "mult": 1.0},
            },
            LegEnum.BACK_LEFT: {
                "alfa_1": {"offset": 90.0, "mult": -1.0},
                "alfa_2": {"offset": 90.0, "mult": 1.0},
                "alfa_3": {"offset": 90.0, "mult": -1.0},
            },
            LegEnum.BACK_RIGHT: {
                "alfa_1": {"offset": 90.0, "mult": -1.0},
                "alfa_2": {"offset": 90.0, "mult": -1.0},
                "alfa_3": {"offset": 90.0, "mult": 1.0},
            },
        }
        # MQTT settings
        self.mmqt_host = "192.168.0.52"
        self.mmqt_topic = "test/topic"
        self.mmqt_sensors = "test/sensors"

        self.client = mqtt.Client()
        self.client.connect(self.mmqt_host)

    def subscribe(self, client: mqtt.Client):

        def on_message(client, userdata, msg):
            payload = msg.payload.decode()  # bytes → str
            data = json.loads(payload)
            i = data["Imu"]["i"]
            j = data["Imu"]["j"]
            k = data["Imu"]["k"]
            w = data["Imu"]["w"]
            sensor = SensorDataMsg({"i": i, "j": j, "k": k, "w": w})
            self.publish(sensor)

        self.client.loop_start()
        client.subscribe(self.mmqt_sensors)
        client.on_message = on_message

    def run_code(self):
        self.subscribe(self.client)
        while True:
            sleep(1)

    def get_topic_type(self):
        return SensorDataMsg

    def handle_ik_result(self, msg: LegAnglesPhaseMsg):
        self.logger.debug(f"Got message {msg}")

        corrected = {}

        for leg, angles in msg.leg_angles.items():
            corrected[leg] = self.correct(leg, angles)

        msg_to_publish = ServoPositionTarget.map(corrected)

        self.publish_to_mmqt(msg_to_publish)

    def publish_to_mmqt(self, data: ServoPositionTarget):
        message = {"Position": data.to_dict()}
        payload = json.dumps(message)

        self.client.publish(self.mmqt_topic, payload)

        pass

    def correct(self, leg: LegEnum, angles: LegAnglesMsg) -> LegAnglesMsg:

        corrections = self.corrections[leg]

        alfa_1_corrected = (
            corrections["alfa_1"]["mult"] * math.degrees(angles.alfa_1)
            + corrections["alfa_1"]["offset"]
        )

        alfa_2_corrected = (
            corrections["alfa_2"]["mult"] * math.degrees(angles.alfa_2)
            + corrections["alfa_2"]["offset"]
        )

        alfa_3_corrected = (
            corrections["alfa_3"]["mult"] * math.degrees(angles.alfa_3)
            + corrections["alfa_3"]["offset"]
        )

        return LegAnglesMsg(alfa_1_corrected, alfa_2_corrected, alfa_3_corrected)
