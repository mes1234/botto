import numpy as np
import pytest
from src.utils.fk import Angles, FK_Leg
from pytest import approx


def test_init_position():
    leg = FK_Leg(1.0, 1.0)
    pos = leg.compute_fk(Angles(0.0, 0.0, 0.0))
    assert pos.x == approx(0.0)
    assert pos.y == approx(0.0)
    assert pos.z == approx(-2.0)


@pytest.mark.parametrize(
    "alfa_1, alfa_2, alfa_3, x,y,z",
    [
        (0.0, 0.0, 0.0, 0.0, 0.0, -2.0),  # neutral position
        # alfa_2 rotations
        (0.0, -np.pi / 2.0, 0.0, 2.0, 0.0, 0.0),
        (0.0, np.pi / 2.0, 0.0, -2.0, 0.0, 0.0),
        # alfa_3 rotations
        (0.0, 0.0, -np.pi / 2.0, 1.0, 0.0, -1.0),
        (0.0, 0.0, np.pi / 2.0, -1.0, 0.0, -1.0),
        (0.0, np.pi / 2.0, np.pi / 2.0, -1.0, 0.0, 1.0),
        # alfa_1 rotations
        (np.pi / 2.0, 0.0, 0.0, 0.0, 2.0, 0.0),
        (np.pi / 2.0, -np.pi / 2.0, 0.0, 2.0, 0.0, 0.0),
        (np.pi / 2.0, 0.0, -np.pi / 2.0, 1.0, 1.0, 0.0),
        (np.pi / 2.0, -np.pi / 2.0, -np.pi / 2.0, 1.0, -1.0, 0.0),
        # random
        (0.0, np.pi / 2.0, np.pi / 2.0, -1.0, 0.0, 1.0),
        (np.pi / 2.0, np.pi / 2.0, np.pi / 2.0, -1.0, -1.0, 0.0),
    ],
)
def test_fk(alfa_1: float, alfa_2: float, alfa_3: float, x: float, y: float, z: float):
    leg = FK_Leg(1.0, 1.0)
    angles = Angles(alfa_1, alfa_2, alfa_3)
    pos = leg.compute_fk(angles)
    actual_x = float(pos.x)
    actual_y = float(pos.y)
    actual_z = float(pos.z)
    assert actual_x == approx(x)
    assert actual_y == approx(y)
    assert actual_z == approx(z)
