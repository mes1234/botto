from time import sleep
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.base.process import BottoProcess
from src.playground.msg.messages import (
    GaitPhaseMsg,
    GaitPhaseWithCorrectionsMsg,
    SensorDataMsg,
)


class Controller(BottoProcess[GaitPhaseWithCorrectionsMsg]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensors = None
        self.sensor_o_i = []
        self.sensor_o_j = []
        self.sensor_o_k = []
        self.sensor_o_w = []

    def run_code(self):
        root = tk.Tk()
        root.title("Offset Control")

        # Create sliders
        self.x_slider = ttk.Scale(
            root, from_=-200, to=200, orient="horizontal", command=self.update_values
        )
        self.y_slider = ttk.Scale(
            root, from_=-200, to=200, orient="horizontal", command=self.update_values
        )
        self.z_slider = ttk.Scale(
            root, from_=-200, to=200, orient="horizontal", command=self.update_values
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

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Sensors vs Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Sensor Values")
        self.ax.grid(True)

        #  trend lines:
        (self.line_i,) = self.ax.plot([], "r-", label="Sensor i")
        (self.line_j,) = self.ax.plot([], "b-", label="Sensor j")
        (self.line_k,) = self.ax.plot([], "g-", label="Sensor k")
        (self.line_w,) = self.ax.plot([], "y-", label="Sensor w")
        self.ax.legend(loc="upper right")

        # Embed the figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        # Start main loop
        root.after(100, self.update_plot)
        root.mainloop()

    def handle_sensors(self, sensors: SensorDataMsg):
        self.sensors = sensors
        self.sensor_o_i.append(sensors.sensor_values["i"])
        self.sensor_o_j.append(sensors.sensor_values["j"])
        self.sensor_o_k.append(sensors.sensor_values["k"])
        self.sensor_o_w.append(sensors.sensor_values["w"])
        # Limit history length to avoid slowing down
        if len(self.sensor_o_i) > 200:
            self.sensor_o_i.pop(0)
            self.sensor_o_j.pop(0)
            self.sensor_o_k.pop(0)
            self.sensor_o_w.pop(0)

    def handle_gait(self, gait_phase: GaitPhaseMsg):

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

    def update_plot(self): 
        x_axis = list(range(len(self.sensor_o_i)))
        self.line_i.set_data(x_axis, self.sensor_o_i)
        self.line_j.set_data(x_axis, self.sensor_o_j)
        self.line_k.set_data(x_axis, self.sensor_o_k)
        self.line_w.set_data(x_axis, self.sensor_o_w)

        # Adjust axes dynamically
        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw_idle()

        # Refresh every 100 ms
        self.canvas.get_tk_widget().after(100, self.update_plot)
