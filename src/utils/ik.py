from concurrent.futures import ProcessPoolExecutor
from typing import List
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
        **kwargs,
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
        data = self.__brute_p__()
        return KDTree(data=data)

    @classmethod
    def _compute_position(cls, args):
        """Helper function for parallel FK computation."""
        self_ref, alfa_1, alfa_2, alfa_3 = args
        angle = Angles(alfa_1, alfa_2, alfa_3)
        position = self_ref.compute_fk(angle)
        return [position.x, position.y, position.z], angle

    def __brute_p__(self) -> NDArray[np.float16]:
        self.angles = []

        # Generate all combinations first
        alfas_1 = np.arange(
            self.alfa_1_limits.lower, self.alfa_1_limits.upper, self.step
        )
        alfas_2 = np.arange(
            self.alfa_2_limits.lower, self.alfa_2_limits.upper, self.step
        )
        alfas_3 = np.arange(
            self.alfa_3_limits.lower, self.alfa_3_limits.upper, self.step
        )

        combos = [
            (self, a1, a2, a3) for a1 in alfas_1 for a2 in alfas_2 for a3 in alfas_3
        ]

        # Run in parallel
        xyz = []
        angles = []

        with ProcessPoolExecutor() as executor:
            for pos, angle in executor.map(
                IK_Leg._compute_position, combos, chunksize=10_000
            ):
                xyz.append(pos)
                angles.append(angle)

        self.angles = angles
        return np.array(xyz, dtype=np.float16)
