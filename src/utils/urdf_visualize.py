import pybullet as p
import pybullet_data
import time


def show_quadruped():
    # Step 1: Generate URDF file
    urdf_file = "quadruped_full.urdf"

    # Step 2: Start PyBullet GUI
    physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.resetDebugVisualizerCamera(
        cameraDistance=1.0,
        cameraYaw=50,
        cameraPitch=-30,
        cameraTargetPosition=[0, 0, 0],
    )
    # Step 3: Load ground and robot
    p.setGravity(0, 0, -9.81)

    plane_id = p.loadURDF("plane.urdf")
    robot_id = p.loadURDF(urdf_file, basePosition=[0, 0, 0.3])
    p.changeDynamics(robot_id, -1, mass=0.001)
    num_joints = p.getNumJoints(robot_id)
    print(f"Robot loaded with {num_joints} joints.")

    # Step 4: Create sliders for each joint
    sliders = []
    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        joint_name = joint_info[1].decode("utf-8")
        sliders.append(
            (joint_name, p.addUserDebugParameter(joint_name, -1.57, 1.57, 0))
        )
    # Step 5: Run the simulation loop
    while True:
        # Read all sliders and set joint positions
        for i, (joint_name, slider_id) in enumerate(sliders):
            target_pos = p.readUserDebugParameter(slider_id)
            p.setJointMotorControl2(
                robot_id, i, p.POSITION_CONTROL, targetPosition=target_pos, force=50
            )
        p.stepSimulation()
        time.sleep(1.0 / 60.0)


if __name__ == "__main__":
    show_quadruped()
