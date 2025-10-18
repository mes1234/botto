from src.playground.processors.gait_generator import GaitGeneratorProcess
from src.playground.processors.ik_resolver import IKResolverProcess
from src.base.host import BottoHost
from src.impl.zero_communicator import BottZeroMqCommunicator
from src.playground.processors.dummy_process import DummyBottoProcess

import src.base.config as config

config.LOG_LEVEL = "INFO"

gait_generator = GaitGeneratorProcess("gait_generator", "gait_phase_topic")
ik_resolver = IKResolverProcess("ik_resolver", "leg_angles_phase_topic")

ik_resolver.register_subscribe_callback(gait_generator, ik_resolver.resolve_ik_handler)

host = BottoHost(BottZeroMqCommunicator)

host = host.attach_process(gait_generator).attach_process(ik_resolver).start()
