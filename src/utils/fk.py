from typing import List, Optional
import numpy as np
from scipy.spatial.transform import Rotation as R


class Position:

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        x_1: Optional[float] = None,
        y_1: Optional[float] = None,
        z_1: Optional[float] = None,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.x_1 = x_1
        self.y_1 = y_1
        self.z_1 = z_1


class Angles:
    def __init__(self, alfa_1: float, alfa_2: float, alfa_3: float):
        self.alfa_1 = alfa_1
        self.alfa_2 = alfa_2
        self.alfa_3 = alfa_3


class FK_Leg:

    def __init__(self, l1: float, l2: float, y0: float, *args, **kwargs):
        self.l1 = l1
        self.l2 = l2
        self.yo = y0
        pass

    def compute_fk(self, angles: Angles) -> Position:

        x1 = self.l1 * np.cos(angles.alfa_2 + np.pi / 2)
        z1 = -self.l1 * np.sin(angles.alfa_2 + np.pi / 2)

        x2 = x1 + self.l2 * np.cos(angles.alfa_3 + np.pi / 2)
        z2 = z1 + -self.l2 * np.sin(angles.alfa_3 + np.pi / 2)

        x1p = x1
        x2p = x2

        y1p = self.yo * np.cos(angles.alfa_1) - z1 * np.sin(angles.alfa_1)
        y2p = self.yo * np.cos(angles.alfa_1) - z2 * np.sin(angles.alfa_1)

        z1p = self.yo * np.sin(angles.alfa_1) + z1 * np.cos(angles.alfa_1)
        z2p = self.yo * np.sin(angles.alfa_1) + z2 * np.cos(angles.alfa_1)

        fk_mid = [x1p, y1p, z1p]
        fk_end = [x2p, y2p, z2p]

        return Position(
            fk_end[0], fk_end[1], fk_end[2], fk_mid[0], fk_mid[1], fk_mid[2]
        )

    def compute_fk1(self, angles: Angles) -> Position:
        # Existing rotations

        # TODO vectorize it
        rot_alfa_1 = R.from_rotvec(np.array([1.0, 0.0, 0.0]) * angles.alfa_1)
        rot_alfa_2 = R.from_rotvec(np.array([0.0, 1.0, 0.0]) * angles.alfa_2)

        # Initial points
        point_mid = np.array([0.0, 0.0, -self.l1])
        point_end = np.array([0.0, 0.0, -self.l1 - self.l2])

        # Apply the first two rotations
        rot12 = rot_alfa_1 * rot_alfa_2
        fk_mid = rot12.apply(point_mid)
        fk_end_pre_rot3 = rot12.apply(point_end)

        # Rotation around y-axis by alfa_3 **around point_mid**
        local_y = rot12.apply([0.0, 1.0, 0.0])
        rot_alfa_3 = R.from_rotvec(local_y * angles.alfa_3)

        # Translate fk_end_pre_rot3 to origin relative to fk_mid
        relative = fk_end_pre_rot3 - fk_mid

        # Rotate relative vector
        rotated_relative = rot_alfa_3.apply(relative)

        # Translate back
        fk_end = fk_mid + rotated_relative

        return Position(
            fk_end[0], fk_end[1], fk_end[2], fk_mid[0], fk_mid[1], fk_mid[2]
        )
