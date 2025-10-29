from time import sleep
import tkinter as tk
from tkinter import ttk
from src.base.process import BottoProcess
from src.playground.msg.messages import GaitPhaseMsg, GaitPhaseWithCorrectionsMsg


class Controller(BottoProcess[GaitPhaseWithCorrectionsMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run_code(self):
        root = tk.Tk()
        root.title("Offset Control")

        # Create sliders
        self.x_slider = ttk.Scale(
            root, from_=-100, to=100, orient="horizontal", command=self.update_values
        )
        self.y_slider = ttk.Scale(
            root, from_=-100, to=100, orient="horizontal", command=self.update_values
        )
        self.z_slider = ttk.Scale(
            root, from_=-100, to=100, orient="horizontal", command=self.update_values
        )

        ttk.Label(root, text="Enable").pack(pady=10)
        self.enable_var = tk.BooleanVar(value=False)
        self.enable_check = ttk.Checkbutton(
            root, text="Enable robot", variable=self.enable_var
        ).pack(pady=10)

        # Create labels
        ttk.Label(root, text="Offset X").pack(pady=(10, 0))
        self.x_slider.pack(fill="x", padx=20)

        ttk.Label(root, text="Offset Y").pack(pady=(10, 0))
        self.y_slider.pack(fill="x", padx=20)

        ttk.Label(root, text="Offset Z").pack(pady=(10, 0))
        self.z_slider.pack(fill="x", padx=20)

        # Display values
        self.value_label = ttk.Label(root, text="Offset X: 0.00, Y: 0.00, Z: 0.00")
        self.value_label.pack(pady=20)

        # Start main loop
        root.mainloop()

    def controller_handler(self, gait_phase: GaitPhaseMsg):

        if not self.enable_var.get():
            self.logger.debug("Controller disabled; passing through GaitPhaseMsg")
            return

        for leg_enum, leg_pos in gait_phase.leg_positions.items():
            leg_pos.x += self.x_slider.get() / 100.0
            leg_pos.y += self.y_slider.get() / 100.0
            leg_pos.z += self.z_slider.get() / 100.0

        phase = GaitPhaseWithCorrectionsMsg(gait_phase.leg_positions)
        self.logger.debug("Received GaitPhaseMsg for control")

        self.publish(phase)

    def get_topic_type(self):
        return GaitPhaseWithCorrectionsMsg

    def update_values(self, event=None):
        x = self.x_slider.get()
        y = self.y_slider.get()
        z = self.z_slider.get()
        self.value_label.config(text=f"Offset X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
