from src.base.process import BottoProcess
from src.playground.msg.messages import GaitPhaseMsg, LegAnglesPhaseMsg


class IKResolverProcess(BottoProcess[LegAnglesPhaseMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        while True:
            # Placeholder for IK resolution logic
            pass

    def get_topic_type(self):
        return LegAnglesPhaseMsg

    def resolve_ik_handler(self, gait_phase: GaitPhaseMsg):
        self.logger.debug("Received GaitPhaseMsg for IK resolution")
