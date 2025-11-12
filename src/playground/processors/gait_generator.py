from src.base.messages import BottoMessage
from src.base.process import BottoProcess
from src.playground.msg.messages import GaitPhaseMsg, LegEnum, LegPositionMsg
from time import sleep
from math import sin


class GaitGeneratorProcess(BottoProcess[GaitPhaseMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        counter = 0
        while True:
            phase = sin(counter) / 10.0 * 2.0
            counter += 1
            gait_phase = self.generate_gait_phase(phase)
            sleep(0.1)  # Simulate processing delay
            self.publish(gait_phase)
            self.logger.debug("Published GaitPhaseMsg")

    def generate_gait_phase(self, cycle: float) -> GaitPhaseMsg:
        # Placeholder for gait phase generation logic
        leg_positions = {
            LegEnum.FRONT_LEFT: LegPositionMsg(0.0, 0.0, -1.7 + cycle),
            LegEnum.FRONT_RIGHT: LegPositionMsg(0.0, 0.0, -1.7 - cycle),
            LegEnum.BACK_LEFT: LegPositionMsg(0.0, 0.0, -1.7 - cycle),
            LegEnum.BACK_RIGHT: LegPositionMsg(0.0, 0.0, -1.7 + cycle),
        }
        self.logger.debug(f"Generated GaitPhaseMsg with cycle value: {-1.7 + cycle}")
        return GaitPhaseMsg(leg_positions)

    def get_topic_type(self):
        return GaitPhaseMsg
