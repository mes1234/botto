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
visualizer = VisualizerProcessor("visualizer", "none_topic")

controller.register_subscribe_callback(gait_generator, controller.controller_handler)
ik_resolver.register_subscribe_callback(controller, ik_resolver.resolve_ik_handler)
visualizer.register_subscribe_callback(ik_resolver, visualizer.visualize_handler)

host = BottoHost(BottZeroMqCommunicator)

host = (
    host.attach_process(gait_generator)
    .attach_process(controller)
    .attach_process(ik_resolver)
    .attach_process(visualizer)
    .start()
)
