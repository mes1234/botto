from src.playground.processors.robot_driver import RobotDriver
from src.playground.processors.controller import Controller
from src.playground.processors.visualizer import VisualizerProcessor
from src.playground.processors.gait_generator import GaitGeneratorProcess
from src.playground.processors.ik_resolver import IKResolverProcess
from src.base.host import BottoHost
from src.impl.zero_communicator import BottZeroMqCommunicator

import src.base.config as config

config.LOG_LEVEL = "INFO"

gait_generator = GaitGeneratorProcess("gait_generator", "gait_phase_topic")
ik_resolver = IKResolverProcess("ik_resolver", "leg_angles_phase_topic")
controller = Controller("controller", "gait_phase_corrections_topic")
visualizer = VisualizerProcessor("visualizer", "visualizer_none_topic")
robot_driver = RobotDriver("robot_driver", "robot_driver_none_topic")

controller.register_subscribe_callback(gait_generator, controller.handle_gait)

controller.register_subscribe_callback(visualizer, controller.handle_sensors)

ik_resolver.register_subscribe_callback(controller, ik_resolver.resolve_ik_handler)

visualizer.register_subscribe_callback(ik_resolver, visualizer.visualize_handler)

robot_driver.register_subscribe_callback(ik_resolver, robot_driver.handle_ik_result)

host = BottoHost(BottZeroMqCommunicator)

host = (
    host.attach_process(gait_generator)
    .attach_process(controller)
    .attach_process(ik_resolver)
    .attach_process(visualizer)
    .attach_process(robot_driver)
    .start()
)
