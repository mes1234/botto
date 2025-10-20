from src.playground.msg.messages import NoneMsg
from src.base.process import BottoProcess
import pybullet as p
import pybullet_data
import time


class VisualizerProcessor(BottoProcess[NoneMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.urdf_file = "quadruped_full.urdf"

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
        while True:
            # Read all sliders and set joint positions
            for i, (joint_name, slider_id) in enumerate(self.sliders):
                target_pos = p.readUserDebugParameter(slider_id)
                p.setJointMotorControl2(
                    self.robot_id,
                    i,
                    p.POSITION_CONTROL,
                    targetPosition=target_pos,
                    force=50,
                )
            p.stepSimulation()
            time.sleep(1.0 / 60.0)

    def get_topic_type(self):
        return NoneMsg
