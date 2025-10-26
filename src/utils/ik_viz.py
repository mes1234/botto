import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.fk import Angles, Position
from src.utils.ik import IK_Leg, IK_Limits


step = np.pi / 180.0  # 1deg resolution
alfa_1_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
alfa_2_limits = IK_Limits(-np.pi / 4.0, np.pi / 4.0)
alfa_3_limits = IK_Limits(0, np.pi / 2.0)
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
# --------------------------------------

# Initial position
x_init, y_init, z_init = 0.0, 0.0, -1.8

# Set up the figure and axes
fig, (ax_xz, ax_zy) = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.25)

# Initial computation
angles = leg.compute_ik([Position(x_init, y_init, z_init)])[0]
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

s_x = Slider(ax_x, "X", -0.5, 0.5, valinit=x_init)
s_y = Slider(ax_y, "Y", -0.5, 0.5, valinit=y_init)
s_z = Slider(ax_z, "Z", -2.0, -1.5, valinit=z_init)


def update(val):
    x = s_x.val
    y = s_y.val
    z = s_z.val

    angles = leg.compute_ik([Position(x, y, z)])[0]
    pos = leg.compute_fk(Angles(angles.alfa_1, angles.alfa_2, angles.alfa_3))

    # For visualization, assume 4 points: origin + 3 joints
    # (You can replace these with your own joint FK positions)
    joints_x = [0, pos.x_1, pos.x]
    joints_y = [0, pos.y_1, pos.y]
    joints_z = [0, pos.z_1, pos.z]

    # Update lines
    line_xz.set_data(joints_x, joints_z)
    line_zy.set_data(joints_z, joints_y)

    fig.canvas.draw_idle()


s_x.on_changed(update)
s_y.on_changed(update)
s_z.on_changed(update)

plt.show()
