from enum import Enum

from src.base.messages import BottoMessage


class LegPositionMsg:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}

    @classmethod
    def from_dict(cls, d: dict) -> "LegPositionMsg":
        return cls(d["x"], d["y"], d["z"])


class LegEnum(Enum):
    FRONT_LEFT = 1
    FRONT_RIGHT = 2
    BACK_LEFT = 3
    BACK_RIGHT = 4


class GaitPhaseMsg(BottoMessage):
    """Message representing the positions of all legs in a gait phase."""

    def __init__(self, leg_positions: dict[LegEnum, LegPositionMsg]):
        self.leg_positions = leg_positions

    def to_dict(self) -> dict:
        # convert enum keys to names for JSON
        return {leg.name: pos.to_dict() for leg, pos in self.leg_positions.items()}

    @classmethod
    def from_dict(cls, d: dict) -> "GaitPhaseMsg":
        return cls(
            {LegEnum[name]: LegPositionMsg.from_dict(pos) for name, pos in d.items()}
        )


class GaitPhaseWithCorrectionsMsg(GaitPhaseMsg):
    """Message representing the positions of all legs in a gait phase with corrections."""

    def __init__(self, leg_positions: dict[LegEnum, LegPositionMsg]):
        super().__init__(leg_positions)


class LegAnglesMsg(BottoMessage):
    """Message representing the joint angles of a leg."""

    def __init__(self, alfa_1: float, alfa_2: float, alfa_3: float):
        self.alfa_1 = alfa_1
        self.alfa_2 = alfa_2
        self.alfa_3 = alfa_3

    def to_dict(self) -> dict:
        return {"alfa_1": self.alfa_1, "alfa_2": self.alfa_2, "alfa_3": self.alfa_3}

    @classmethod
    def from_dict(cls, d: dict) -> "LegAnglesMsg":
        return cls(d["alfa_1"], d["alfa_2"], d["alfa_3"])


class LegAnglesPhaseMsg(BottoMessage):
    """Message representing the joint angles of all legs in a gait phase."""

    def __init__(self, leg_angles: dict[LegEnum, LegAnglesMsg]):
        self.leg_angles = leg_angles

    def to_dict(self) -> dict:
        return {leg.name: ang.to_dict() for leg, ang in self.leg_angles.items()}

    @classmethod
    def from_dict(cls, d: dict) -> "LegAnglesPhaseMsg":
        return cls(
            {LegEnum[name]: LegAnglesMsg.from_dict(ang) for name, ang in d.items()}
        )


class NoneMsg(BottoMessage):
    """Message representing no data."""

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, d: dict) -> "NoneMsg":
        return cls()
