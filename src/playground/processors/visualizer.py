from src.playground.msg.messages import (
    LegAnglesMsg,
    LegAnglesPhaseMsg,
    LegEnum,
    NoneMsg,
)
from src.base.process import BottoProcess
import pybullet as p
import pybullet_data
import time


class VisualizerProcessor(BottoProcess[NoneMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urdf_file = "quadruped_full.urdf"

        self.joints = {
            "base_joint": 0.0,
            "base_link_to_fl_hip": 0.0,
            "fl_hip_to_fl_knee": 0.0,
            "fl_knee_to_fl_foot": 0.0,
            "base_link_to_fr_hip": 0.0,
            "fr_hip_to_fr_knee": 0.0,
            "fr_knee_to_fr_foot": 0.0,
            "base_link_to_rr_hip": 0.0,
            "rr_hip_to_rr_knee": 0.0,
            "rr_knee_to_rr_foot": 0.0,
            "base_link_to_rl_hip": 0.0,
            "rl_hip_to_rl_knee": 0.0,
            "rl_knee_to_rl_foot": 0.0,
        }

    def run_code(self):
        # Step 2: Start PyBullet GUI
        self.physics_client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetDebugVisualizerCamera(
            cameraDistance=3.0,
            cameraYaw=50,
            cameraPitch=-30,
            cameraTargetPosition=[0, 0, 0],
        )
        # Step 3: Load ground and robot
        p.setGravity(0, 0, -9.81)

        self.plane_id = p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF(self.urdf_file, basePosition=[0, 0, 0.3])
        num_joints = p.getNumJoints(self.robot_id)
        self.logger.info(f"Robot loaded with {num_joints} joints.")

        # Step 4: Create sliders for each joint
        self.sliders = []
        for i in range(num_joints):
            joint_info = p.getJointInfo(self.robot_id, i)
            joint_name = joint_info[1].decode("utf-8")
            self.sliders.append(
                (joint_name, p.addUserDebugParameter(joint_name, -1.57, 1.57, 0))
            )
            self.logger.info(f"Slider created for joint: {joint_name}")

        forces = [50] * (num_joints)
        ii = list(range(num_joints))
        positions = [0] * (num_joints)
        names = [
            p.getJointInfo(self.robot_id, i)[1].decode("utf-8")
            for i in range(num_joints)
        ]

        while True:
            positions = [self.joints[name] for name in names]
            p.setJointMotorControlArray(
                self.robot_id,
                ii,
                p.POSITION_CONTROL,
                targetPositions=positions,
                forces=forces,
            )

            p.stepSimulation()
            time.sleep(1.0 / 250.0)

    def get_topic_type(self):
        return NoneMsg

    def visualize_handler(self, msg: LegAnglesPhaseMsg):
        self.logger.debug("Received LegAnglesMsg for visualization")
        for leg_enum, angles_msg in msg.leg_angles.items():
            if leg_enum == LegEnum.FRONT_LEFT:
                self.joints["base_link_to_fl_hip"] = angles_msg.alfa_1
                self.joints["fl_hip_to_fl_knee"] = angles_msg.alfa_2
                self.joints["fl_knee_to_fl_foot"] = angles_msg.alfa_3
            elif leg_enum == LegEnum.FRONT_RIGHT:
                self.joints["base_link_to_fr_hip"] = angles_msg.alfa_1
                self.joints["fr_hip_to_fr_knee"] = angles_msg.alfa_2
                self.joints["fr_knee_to_fr_foot"] = angles_msg.alfa_3
            elif leg_enum == LegEnum.BACK_LEFT:
                self.joints["base_link_to_rl_hip"] = angles_msg.alfa_1
                self.joints["rl_hip_to_rl_knee"] = angles_msg.alfa_2
                self.joints["rl_knee_to_rl_foot"] = angles_msg.alfa_3
            elif leg_enum == LegEnum.BACK_RIGHT:
                self.joints["base_link_to_rr_hip"] = angles_msg.alfa_1
                self.joints["rr_hip_to_rr_knee"] = angles_msg.alfa_2
                self.joints["rr_knee_to_rr_foot"] = angles_msg.alfa_3
        pass
