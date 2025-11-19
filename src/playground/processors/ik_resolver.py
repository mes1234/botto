from typing import List
import numpy as np
from src.base.process import BottoProcess
from src.playground.msg.messages import (
    GaitPhaseWithCorrectionsMsg,
    LegAnglesMsg,
    LegAnglesPhaseMsg,
    LegEnum,
)
from time import sleep

from src.utils.ik import IK_Leg, IK_Limits
from src.utils.fk import Angles, Position


class IKResolverProcess(BottoProcess[LegAnglesPhaseMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        step = np.pi / 180.0 * 2.0  # 2deg resolution
        alfa_1_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
        alfa_2_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
        alfa_3_limits = IK_Limits(0.0, np.pi / 2.0)
        l_1 = 1.0
        l_2 = 1.49
        y0 = 0.0
        k = 1
        self.leg = IK_Leg(
            step,
            alfa_1_limits=alfa_1_limits,
            alfa_2_limits=alfa_2_limits,
            alfa_3_limits=alfa_3_limits,
            k=k,
            l1=l_1,
            l2=l_2,
            y0=y0,
        )

    def run_code(self):
        while True:
            # Placeholder for IK resolution logic
            sleep(10)  # Simulate long processing delay
            pass

    def get_topic_type(self):
        return LegAnglesPhaseMsg

    def resolve_ik_handler(self, gait_phase: GaitPhaseWithCorrectionsMsg):
        phase = IKResolverProcess.remap(
            self.leg.compute_ik(IKResolverProcess.map(gait_phase))
        )
        self.logger.debug("Received GaitPhaseWithCorrectionsMsg for IK resolution")

        self.publish(phase)

    @classmethod
    def map(cls, gait_phase: GaitPhaseWithCorrectionsMsg) -> List[Position]:
        positions = []
        for leg_enum in LegEnum:
            leg_pos_msg = gait_phase.leg_positions[leg_enum]
            positions.append(Position(leg_pos_msg.x, leg_pos_msg.y, leg_pos_msg.z))
        return positions

    @classmethod
    def remap(cls, angles: List[Angles]) -> LegAnglesPhaseMsg:
        phase = {}
        for leg, angle in zip(LegEnum, angles):
            phase[leg] = LegAnglesMsg(angle.alfa_1, angle.alfa_2, angle.alfa_3)
        return LegAnglesPhaseMsg(phase)
