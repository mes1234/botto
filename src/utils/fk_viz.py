import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.fk import Angles, FK_Leg, Position
from src.utils.ik import IK_Leg, IK_Limits


step = np.pi / 180.0  # 1deg resolution
alfa_1_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
alfa_2_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
alfa_3_limits = IK_Limits(-np.pi / 2.0, 0)
l_1 = 1.0
l_2 = 1.0
y0 = 0.2
k = 1
leg = FK_Leg(l1=l_1, l2=l_2, y0=y0)
# --------------------------------------

# Initial position
angles = Angles(0.0, 0.0, 0.0)

# Set up the figure and axes
fig, (ax_xz, ax_zy) = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.25)

# Initial computation
pos = leg.compute_fk(Angles(angles.alfa_1, angles.alfa_2, angles.alfa_3))

# Plot placeholders for both planes
(line_xz,) = ax_xz.plot([], [], "o-", lw=3, color="tab:blue")
(line_zy,) = ax_zy.plot([], [], "o-", lw=3, color="tab:green")

ax_xz.set_xlim(-4, 4)
ax_xz.set_ylim(-4, 4)
ax_xz.set_xlabel("X")
ax_xz.set_ylabel("Z")
ax_xz.set_title("XZ Plane")

ax_zy.set_xlim(-4, 4)
ax_zy.set_ylim(-4, 4)
ax_zy.set_xlabel("Z")
ax_zy.set_ylabel("Y")
ax_zy.set_title("ZY Plane")

# Slider axes
ax_x = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_y = plt.axes([0.2, 0.06, 0.65, 0.03])
ax_z = plt.axes([0.2, 0.02, 0.65, 0.03])

s_a1 = Slider(ax_x, "alfa_1", -np.pi / 2.0, np.pi / 2.0, valinit=angles.alfa_1)
s_a2 = Slider(ax_y, "alfa_2", -np.pi / 2.0, np.pi / 2.0, valinit=angles.alfa_2)
s_a3 = Slider(ax_z, "alfa_3", -np.pi / 2.0, np.pi / 2.0, valinit=angles.alfa_3)


def update(val):
    a1 = s_a1.val
    a2 = s_a2.val
    a3 = s_a3.val

    pos = leg.compute_fk(Angles(a1, a2, a3))

    # For visualization, assume 4 points: origin + 3 joints
    # (You can replace these with your own joint FK positions)
    joints_x = [0, pos.x_1, pos.x]
    joints_y = [0, pos.y_1, pos.y]
    joints_z = [0, pos.z_1, pos.z]

    # Update lines
    line_xz.set_data(joints_x, joints_z)
    line_zy.set_data(joints_z, joints_y)

    fig.canvas.draw_idle()


s_a1.on_changed(update)
s_a2.on_changed(update)
s_a3.on_changed(update)

plt.show()
