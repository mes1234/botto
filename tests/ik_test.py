import numpy as np
import pytest
from src.utils.fk import Position
from src.utils.ik import IK_Limits, IK_Leg
from pytest import approx


def test_init_position():
    step = np.pi / 180.0  # 2deg resolution
    alfa_1_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
    alfa_2_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
    alfa_3_limits = IK_Limits(0.0, np.pi / 2.0)
    l_1 = 1.0
    l_2 = 1.0
    k = 1
    leg = IK_Leg(
        step,
        alfa_1_limits=alfa_1_limits,
        alfa_2_limits=alfa_2_limits,
        alfa_3_limits=alfa_3_limits,
        k=k,
        l1=l_1,
        l2=l_2,
    )

    result = leg.compute_ik([Position(0.0, 0.0, -2.0)])[0]

    actual_alfa_1 = result.alfa_1
    actual_alfa_2 = result.alfa_2
    actual_alfa_3 = result.alfa_3
    assert actual_alfa_1 == approx(0.0, abs=step)
    assert actual_alfa_2 == approx(0.0, abs=step)
    assert actual_alfa_3 == approx(0.0, abs=step)
