import math
from src.base.messages import BottoMessage
from src.base.process import BottoProcess
from src.playground.msg.messages import GaitPhaseMsg, LegEnum, LegPositionMsg
from time import sleep
from math import sin


class GaitGeneratorProcess(BottoProcess[GaitPhaseMsg]):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Gait configuration
        self.frequency = 1.0  # steps per second
        self.duty_factor = 0.5 * math.pi * 2  # % of cycle in stance
        self.step_height = 0.2
        self.step_length = 0.5

        # Phase offsets (walk)
        self.offset = {
            LegEnum.FRONT_LEFT: 0.0,
            LegEnum.FRONT_RIGHT: 0.5,
            LegEnum.BACK_LEFT: 0.5,
            LegEnum.BACK_RIGHT: 0.0,
        }

    def run_code(self):
        counter = 0
        while True:
            if counter == 100:
                counter = 0
            counter += 10
            gait_phase = self.generate_gait_phase(counter / 100)
            sleep(0.1)  # Simulate processing delay
            self.publish(gait_phase)
            self.logger.debug("Published GaitPhaseMsg")

    def generate_gait_phase(self, cycle: float) -> GaitPhaseMsg:
        # cycle in range [0..1]
        leg_positions = {}

        for leg, offset in self.offset.items():
            # leg_cycle 0 - 2* pi
            offseted = (cycle + offset) % 1.0
            leg_cycle = offseted * 2 * math.pi

            x = math.sin(leg_cycle + math.pi / 2.0) * self.step_length

            if leg_cycle > self.duty_factor:
                z = -2.2
            else:
                z = -2.2 - math.cos(leg_cycle + math.pi / 2.0) * self.step_height

            leg_positions[leg] = LegPositionMsg(x, 0.0, z)

        return GaitPhaseMsg(leg_positions)

    def get_topic_type(self):
        return GaitPhaseMsg
