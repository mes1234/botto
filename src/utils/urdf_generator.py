import numpy as np
from urchin import (
    URDF,
    Cylinder,
    JointLimit,
    Link,
    Joint,
    Visual,
    Collision,
    Geometry,
    Material,
    Inertial,
    Box,
    xyz_rpy_to_matrix,
)


def create_inertial(mass, ixx, iyy, izz):
    """Helper to create a simple diagonal inertia matrix."""
    return Inertial(
        mass=mass, inertia=[[ixx, 0, 0], [0, iyy, 0], [0, 0, izz]], origin=np.eye(4)
    )


def create_leg(name, base_parent, base_position, link_length, link_radius):
    """Create one leg (3 links + 3 joints)."""
    bx, by, bz = base_position

    # Materials
    mat_hip = Material("blue", color=[0, 0, 1, 1])
    mat_thigh = Material("green", color=[0, 1, 0, 1])
    mat_calf = Material("red", color=[1, 0, 0, 1])

    # Inertial estimates (roughly cylindrical)
    hip_inertial = create_inertial(0.2, 0.001, 0.001, 0.001)
    thigh_inertial = create_inertial(0.2, 0.002, 0.002, 0.002)
    calf_inertial = create_inertial(0.1, 0.001, 0.001, 0.001)

    # Links with visuals, collisions, and inertials
    hip_link = Link(
        name=f"{name}_hip",
        visuals=[
            Visual(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["hip"], radius=link_radius)
                ),
                material=mat_hip,
            )
        ],
        collisions=[
            Collision(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["hip"], radius=link_radius)
                ),
                name=f"{name}_hip_collision",
                origin=np.eye(4),
            )
        ],
        inertial=hip_inertial,
    )

    thigh_link = Link(
        name=f"{name}_thigh",
        visuals=[
            Visual(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["thigh"], radius=link_radius)
                ),
                material=mat_thigh,
            )
        ],
        collisions=[
            Collision(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["thigh"], radius=link_radius)
                ),
                name=f"{name}_thigh_collision",
                origin=np.eye(4),
            )
        ],
        inertial=thigh_inertial,
    )

    calf_link = Link(
        name=f"{name}_calf",
        visuals=[
            Visual(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["calf"], radius=link_radius)
                ),
                material=mat_calf,
            )
        ],
        collisions=[
            Collision(
                geometry=Geometry(
                    cylinder=Cylinder(length=link_length["calf"], radius=link_radius)
                ),
                name=f"{name}_calf_collision",
                origin=np.eye(4),
            )
        ],
        inertial=calf_inertial,
    )

    # Joints

    hip_joint = Joint(
        name=f"{name}_hip_joint",
        parent=base_parent,
        child=f"{name}_hip",
        joint_type="revolute",
        origin=np.array([[1, 0, 1, bx], [0, 1, 0, by], [-1, 0, 1, bz], [0, 0, 0, 1]]),
        axis=[0, 0, 1],
        limit=JointLimit(lower=-1.57, upper=1.57, effort=5, velocity=2),
    )

    thigh_joint = Joint(
        name=f"{name}_thigh_joint",
        parent=f"{name}_hip",
        child=f"{name}_thigh",
        joint_type="revolute",
        origin=np.array(
            [[1, 0, -1, 0], [0, 1, 0, 0], [1, 0, 1, -link_length["hip"]], [0, 0, 0, 1]]
        ),
        axis=[0, 1, 0],
        limit=JointLimit(lower=-1.57, upper=1.57, effort=5, velocity=2),
    )

    calf_joint = Joint(
        name=f"{name}_calf_joint",
        parent=f"{name}_thigh",
        child=f"{name}_calf",
        joint_type="revolute",
        origin=np.array(
            [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -link_length["thigh"]], [0, 0, 0, 1]]
        ),
        axis=[0, 1, 0],
        limit=JointLimit(lower=-1.57, upper=1.57, effort=5, velocity=2),
    )

    links = [hip_link, thigh_link, calf_link]
    joints = [hip_joint, thigh_joint, calf_joint]
    return links, joints


def generate_quadruped_urdf(filename="quadruped_full.urdf"):
    """Generate quadrupedal URDF with visuals, collisions, and inertials."""
    link_length = {"hip": 0.1, "thigh": 0.2, "calf": 0.2}
    link_radius = 0.02

    # Base link
    base_inertial = create_inertial(5.0, 0.05, 0.05, 0.05)
    base_link = Link(
        name="base_link",
        visuals=[
            Visual(
                geometry=Geometry(box=Box(size=[0.3, 0.2, 0.05])),
                material=Material("gray", color=[0.6, 0.6, 0.6, 1.0]),
            )
        ],
        collisions=[
            Collision(
                geometry=Geometry(box=Box(size=[0.3, 0.2, 0.05])),
                name="base_collision",
                origin=np.eye(4),
            )
        ],
        inertial=base_inertial,
    )

    # Leg base positions
    base_positions = {
        "front_left": [0.15, 0.10, 0.0],
        "front_right": [0.15, -0.10, 0.0],
        "rear_left": [-0.15, 0.10, 0.0],
        "rear_right": [-0.15, -0.10, 0.0],
    }

    links = [base_link]
    joints = []

    for leg_name, pos in base_positions.items():
        leg_links, leg_joints = create_leg(
            leg_name, "base_link", pos, link_length, link_radius
        )
        links += leg_links
        joints += leg_joints

    robot = URDF(name="quadruped", links=links, joints=joints)
    robot.save(filename)
    print(f"✅ Saved URDF with inertials: {filename}")


if __name__ == "__main__":
    generate_quadruped_urdf()
