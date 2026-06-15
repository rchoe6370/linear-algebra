# todo
# show/hide connectors 
# angle between a and b 
# snap toggle checkbox 



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, CheckButtons
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def mag(self):
        return np.sqrt(self.x **  + self.y ** 2)

    def project_onto(self, other):
        denom = other.x ** 2 + other.y ** 2
        if denom == 0:
            return Vector(0.0, 0.0)
        scalar = self.dot(other) / denom
        return Vector(scalar * other.x, scalar * other.y)

    def coord(self):
        return f"({self.x:.2f}, {self.y:.2f})"
    
class DrawnVector:
    def __init__(self, ax, vector, name, color):
        self.ax = ax
        self.vector = vector
        self.name = name
        self.color = color

        self.point, = ax.plot(vector.x, vector.y, marker="o", color=color, markersize=10, zorder=5)

        self.line, = ax.plot([0, vector.x], [0, vector.y], color=color, linestyle="-", linewidth=1.8)

        mid_x, mid_y = vector.x / 2, vector.y / 2
        self.label_name = ax.text(mid_x + 0.3, mid_y + 0.3, name, fontsize=10, color=color, fontweight="bold")

        self.label_coord = ax.text(vector.x + 0.3, vector.y + 0.3, vector.coord(), fontsize=8, color=color)

    def update(self, new_vector):
        self.vector = new_vector
        x, y = new_vector.x, new_vector.y

        self.point.set_data([x], [y])
        self.line.set_data([0, x], [0, y])
        self.label_name.set_position((x / 2 + 0.3, y / 2 + 0.3))
        self.label_coord.set_position((x + 0.3, y + 0.3))
        self.label_coord.set_text(new_vector.coord())
    
    def click(self, mouse_x, mous_y):
        dx = mouse_x - self.vector.x
        dy = mous_y - self.vector.y
        return math.sqrt(dx ** 2 + dy ** 2) < 0.4
    
class ResultVector(DrawnVector):
    def update(self, new_vector, label_text):
            super().update(new_vector)
            self.label_name.set_text(label_text)
            self.label_name.set_position((new_vector.x / 2 + 0.3, new_vector.y / 2 + 0.3))

class DrawnConnector:
    def __init__(self, ax, vec_from, vec_to, color="gray"):
        self.vec_from = vec_from
        self.vec_to = vec_to

        self.line, = ax.plot([vec_from.vector.x, vec_to.vector.x], [vec_from.vector.y, vec_to.vector.y], color=color, linestyle="--", linewidth=1.2, alpha=0.6)
    
    def update(self):
        self.line.set_data([self.vec_from.vector.x, self.vec_to.vector.x], [self.vec_from.vector.y, self.vec_to.vector.y])

class VectorEngine:
    operations = ("Addition", "Subtraction", "Projection")

    def __init__(self):
        self.vec_a = Vector(-1.0, 1.0)
        self.vec_b = Vector(2.0, 2.0)
        self.operation = "Addition"
        self.dragging = None

        self.build_figure()
        self.build_drawn_vectors()
        self.connect_events()
        self.refresh()

    def reset(self, event=None):
        self.vec_a = Vector(-1.0, 1.0)
        self.vec_b = Vector(2.0, 2.0)
        self.operation = "Addition"
        self.radio.set_active(0)
        self.dragging = None


    def build_figure(self):
        self.fig = plt.figure(figsize=(7, 6))

        self.ax = self.fig.add_axes([0.28, 0.1, 0.68, 0.82])
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.4)
        self.ax.axhline(0, color="black", linewidth=0.6)
        self.ax.axvline(0, color="black", linewidth=0.6)
        self.ax.set_title("Vector Engine", fontsize=12)

        ax_radio = self.fig.add_axes([0.02, 0.35, 0.20, 0.3])
        self.radio = RadioButtons(ax_radio, self.operations, active=0, activecolor="steelblue")
        self.radio.on_clicked(self.on_operation_change)

        ax_button = self.fig.add_axes([0.08, 0.20, 0.08, 0.06])
        self.button = Button(ax_button, "Reset", hovercolor="steelblue")
        self.button.on_clicked(self.reset)
    
    def build_drawn_vectors(self):
        self.drawn_a = DrawnVector(self.ax, self.vec_a, "A", "firebrick")
        self.drawn_b = DrawnVector(self.ax, self.vec_b, "B", "steelblue")

        result_vec = self.vec_a + self.vec_b
        self.drawn_result = ResultVector(self.ax, result_vec, "A + B", "seagreen")

        self.connector_a_result = DrawnConnector(self.ax, self.drawn_a, self.drawn_result)
        self.connector_b_result = DrawnConnector(self.ax, self.drawn_b, self.drawn_result)


    def compute_result(self):
        if self.operation == "Addition":
            return self.vec_a + self.vec_b, "A + B"
        elif self.operation == "Subtraction":
            return self.vec_a - self.vec_b, "A - B"
        elif self.operation == "Projection":
            return self.vec_a.project_onto(self.vec_b), "A onto B"

    def refresh(self):
        self.drawn_a.update(self.vec_a)
        self.drawn_b.update(self.vec_b)

        result_vec, label = self.compute_result()
        self.drawn_result.update(result_vec, label)

        self.connector_a_result.update()
        self.connector_b_result.update()

        self.fig.canvas.draw_idle()

    def on_operation_change(self, label):
        self.operation = label
        self.refresh()

    def on_press(self, event):
        if event.inaxes != self.ax or event.xdata is None:
            return
        mx, my = event.xdata, event.ydata
        if self.drawn_a.click(mx, my):
            self.dragging = "A"
        elif self.drawn_b.click(mx, my):
            self.dragging = "B"

    def on_motion(self, event):
        if self.dragging is None or event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return
        new_vec = Vector(event.xdata, event.ydata)
        if self.dragging == "A":
            self.vec_a = new_vec
        else:
            self.vec_b = new_vec
        self.refresh()

    def on_release(self, event):
        if self.dragging == "A":
            self.vec_a = self.snap(self.vec_a)
        elif self.dragging == "B":
            self.vec_b = self.snap(self.vec_b)
        
        self.dragging = None
        self.refresh()
    
    def snap(self, vec):
        return Vector(round(vec.x * 2) / 2, round(vec.y * 2) / 2)

    def connect_events(self):
        self.fig.canvas.mpl_connect("button_press_event",  self.on_press)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)

    def run(self):
        plt.show()


if __name__ == "__main__":
    engine = VectorEngine()
    engine.run()