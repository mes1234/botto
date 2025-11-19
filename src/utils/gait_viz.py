import math
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.playground.processors.gait_generator import GaitGeneratorProcess
from src.playground.msg.messages import LegEnum
from matplotlib import pyplot as plt

cycle = [i for i in range(100)]


gait_generator = GaitGeneratorProcess("gait_generator", "gait_phase_topic")


x = []
y = []
z = []
for c in cycle:
    pos = gait_generator.generate_gait_phase(c / 100)
    leg_in_q = pos.leg_positions[LegEnum.BACK_LEFT]
    x.append(leg_in_q.x)
    y.append(leg_in_q.y)
    z.append(leg_in_q.z)
plt.scatter(x, z)
plt.show()
