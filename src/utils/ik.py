from typing import List, Optional
from scipy.spatial import KDTree
import numpy as np
from numpy.typing import NDArray
from src.utils.fk import Angles, FK_Leg, Position


class IK_Limits:
    def __init__(self, lower: float, upper: float) -> None:
        self.lower = lower
        self.upper = upper
        pass


class IK_Leg(FK_Leg):
    def __init__(
        self,
        step: float,
        alfa_1_limits: IK_Limits,
        alfa_2_limits: IK_Limits,
        alfa_3_limits: IK_Limits,
        k: int,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.step = step
        self.alfa_1_limits = alfa_1_limits
        self.alfa_2_limits = alfa_2_limits
        self.alfa_3_limits = alfa_3_limits
        self.k = k

        self.tree = self.__build__()

    def compute_ik(self, positions: List[Position]) -> List[Angles]:
        query = []
        for position in positions:
            query.append([position.x, position.y, position.z])

        dd, ii = self.tree.query(query, self.k, workers=-1)

        result = []

        for item in ii:  # type: ignore
            result.append(self.angles[item])

        return result

    def __build__(self) -> KDTree:
        data = self.__brute__()
        return KDTree(data=data)

    def __brute__(self) -> NDArray[np.float16]:
        self.angles = []
        xyz = []
        for alfa_1 in np.arange(
            self.alfa_1_limits.lower, self.alfa_1_limits.upper, self.step
        ):
            for alfa_2 in np.arange(
                self.alfa_2_limits.lower, self.alfa_2_limits.upper, self.step
            ):
                for alfa_3 in np.arange(
                    self.alfa_3_limits.lower, self.alfa_3_limits.upper, self.step
                ):
                    angle = Angles(
                        alfa_1=float(alfa_1), alfa_2=float(alfa_2), alfa_3=float(alfa_3)
                    )
                    position = self.compute_fk(angle)
                    xyz.append([position.x, position.y, position.z])
                    self.angles.append(angle)
        return np.array(xyz)
