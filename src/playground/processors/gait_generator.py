from src.base.messages import BottoMessage
from src.base.process import BottoProcess
from src.playground.msg.messages import GaitPhaseMsg, LegEnum, LegPositionMsg


class GaitGeneratorProcess(BottoProcess[GaitPhaseMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        while True:
            gait_phase = self.generate_gait_phase()
            self.publish(gait_phase)
            self.logger.debug("Published GaitPhaseMsg")

    def generate_gait_phase(self) -> GaitPhaseMsg:
        # Placeholder for gait phase generation logic
        leg_positions = {
            LegEnum.FRONT_LEFT: LegPositionMsg(1.0, 0.0, 0.0),
            LegEnum.FRONT_RIGHT: LegPositionMsg(0.0, 1.0, 0.0),
            LegEnum.BACK_LEFT: LegPositionMsg(0.0, 0.0, 1.0),
            LegEnum.BACK_RIGHT: LegPositionMsg(0.0, 2.0, 0.0),
        }
        return GaitPhaseMsg(leg_positions)

    def get_topic_type(self):
        return GaitPhaseMsg
