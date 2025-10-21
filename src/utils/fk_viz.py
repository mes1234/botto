import warnings

warnings.filterwarnings(
    "ignore", message=".*missing ScriptRunContext.*"
)  # Suppress Streamlit warning

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from fk import FK_Leg  # Your FK_Leg and Position classes

# --- Initialize leg ---
leg = FK_Leg(l1=1.0, l2=1.0)

st.set_page_config(page_title="FK Leg Visualizer", page_icon="🤖", layout="centered")

st.title("🤖 Forward Kinematics Leg Visualizer")
st.write(
    "Use the sliders below to adjust joint angles α₁, α₂, α₃ and visualize the leg configuration in 3D."
)

# --- Angle sliders ---
alfa_1 = st.slider("α₁ (rotation around X)", -np.pi, np.pi, 0.0, 0.1)
alfa_2 = st.slider("α₂ (rotation around Y)", -np.pi, np.pi, 0.0, 0.1)
alfa_3 = st.slider("α₃ (rotation around local Y at joint 2)", -np.pi, np.pi, 0.0, 0.1)

# --- Compute forward kinematics ---
pos = leg.compute_fk(alfa_1, alfa_2, alfa_3)

# Joint positions
base = np.array([0.0, 0.0, 0.0])
mid = np.array([pos.x_1, pos.y_1, pos.z_1])
end = np.array([pos.x, pos.y, pos.z])

# --- 3D plot using Plotly ---
fig = go.Figure()

# Link 1
fig.add_trace(
    go.Scatter3d(
        x=[base[0], mid[0]],
        y=[base[1], mid[1]],
        z=[base[2], mid[2]],
        mode="lines+markers",
        line=dict(color="royalblue", width=8),
        marker=dict(size=6, color="blue"),
        name="Link 1",
    )
)

# Link 2
fig.add_trace(
    go.Scatter3d(
        x=[mid[0], end[0]],
        y=[mid[1], end[1]],
        z=[mid[2], end[2]],
        mode="lines+markers",
        line=dict(color="orange", width=8),
        marker=dict(size=6, color="red"),
        name="Link 2",
    )
)

# End effector marker
fig.add_trace(
    go.Scatter3d(
        x=[end[0]],
        y=[end[1]],
        z=[end[2]],
        mode="markers+text",
        marker=dict(size=8, color="green"),
        text=["End Effector"],
        textposition="top center",
    )
)

# --- Layout settings ---
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[-2, 2], title="X"),
        yaxis=dict(range=[-2, 2], title="Y"),
        zaxis=dict(range=[-2, 2], title="Z"),
        aspectmode="cube",
    ),
    width=700,
    height=700,
    showlegend=True,
)

st.plotly_chart(fig, use_container_width=True)

# --- Display numerical positions ---
st.subheader("Joint Positions")
st.write(f"**Mid Joint:** (x₁={mid[0]:.3f}, y₁={mid[1]:.3f}, z₁={mid[2]:.3f})")
st.write(f"**End Effector:** (x={end[0]:.3f}, y={end[1]:.3f}, z={end[2]:.3f})")
