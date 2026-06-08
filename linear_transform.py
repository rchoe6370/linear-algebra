# add dashed lines between a b and result of addition and subtraciton
# add subtaciton
# add projeciton

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

def main():

    fig = plt.figure(figsize=(6, 6))

    ax_graph = fig.add_axes([0.3, 0.1, 0.65, 0.8])
    ax_radio = fig.add_axes([0.05, 0.3, 0.18, 0.3])

    radio = RadioButtons(ax_radio, ["Addition", "Subtraction", "Projection"], active=0, activecolor='blue')
    
    def change_operation(label):
        operation = label
        print(operation)

    radio.on_clicked(change_operation)
    
    ax_graph.set_xlim(-5, 5)
    ax_graph.set_ylim(-5, 5)

    ax_graph.grid(True)

    ax_graph.locator_params(axis='both', nbins=5)

    is_dragging = False

    a_initial_x = -1
    a_initial_y = 1

    b_initial_x = 2
    b_initial_y = 2

    add_initial_x = a_initial_x + b_initial_x
    add_initial_y = a_initial_y + b_initial_y

    point_a, = ax_graph.plot(a_initial_x, a_initial_y, marker="o", color="firebrick", markersize=10, picker=True) 
    point_b, = ax_graph.plot(b_initial_x, b_initial_y, marker="o", color="blue", markersize=10, picker=True) 
    point_add, = ax_graph.plot(add_initial_x, add_initial_y, marker="*", color="green", markersize=10)
    
    label_a = ax_graph.text(a_initial_x/2+0.5, a_initial_y/2+0.5, "A", fontsize=10, color="firebrick")
    label_b = ax_graph.text(b_initial_x/2+0.5, b_initial_y/2+0.5, "B", fontsize=10, color="blue")
    label_add = ax_graph.text(add_initial_x/2+0.5, add_initial_y/2+0.5, "A + B", fontsize=10, color="green")

    label_a_coord = ax_graph.text(a_initial_x+0.5, a_initial_y+0.5, f"({a_initial_x:.2f}, {a_initial_y:.2f})", fontsize=10, color="firebrick")   
    label_b_coord = ax_graph.text(b_initial_x+0.5, b_initial_y+0.5, f"({b_initial_x:.2f}, {b_initial_y:.2f})", fontsize=10, color="blue")
    label_add_coord = ax_graph.text(add_initial_x+0.5, add_initial_y+0.5, f"({add_initial_x:.2f}, {add_initial_y:.2f})", fontsize=10, color="green")

    a_xpoints = [0, a_initial_x]
    a_ypoints = [0, a_initial_y]

    b_xpoints = [0, b_initial_x]
    b_ypoints = [0, b_initial_y]

    add_xpoints = [0, a_xpoints[1] + b_xpoints[1]]
    add_ypoints = [0, a_ypoints[1] + b_ypoints[1]]

    line_a, = ax_graph.plot(a_xpoints, a_ypoints, color="firebrick", linestyle="-")
    line_b, = ax_graph.plot(b_xpoints, b_ypoints, color="blue", linestyle="-")
    line_add, = ax_graph.plot(add_xpoints, add_ypoints, color="green", linestyle="-")

    def on_pick(event):
        if event.inaxes != ax_graph: 
            return
        
        nonlocal is_dragging
        global a_x, a_y, b_x, b_y
        a_x = point_a.get_xdata()[0]
        a_y = point_a.get_ydata()[0]
        b_x = point_b.get_xdata()[0]
        b_y = point_b.get_ydata()[0]

        if abs(event.xdata - a_x) < 0.5 and abs(event.ydata - a_y < 0.5):
            is_dragging = "A"
        elif abs(event.xdata - b_x) < 0.5 and abs(event.ydata - b_y  < 0.5):
            is_dragging = "B"
    
    def on_motion(event):
        if not is_dragging or event.inaxes != ax_graph:
            return
        
        new_x = event.xdata
        new_y = event.ydata

        if (is_dragging == "A"):
            label_a_coord.set_position((new_x+0.5, new_y+0.5))
            label_a_coord.set_text(f"({new_x:.2f}, {new_y:.2f})")

            label_a.set_position((new_x/2+0.5, new_y/2+0.5))
            
            point_a.set_data([new_x], [new_y])

            a_xpoints[1] = new_x
            a_ypoints[1] = new_y

            line_a.set_data([a_xpoints], [a_ypoints])

            new_x_add = new_x + b_x
            new_y_add = new_y + b_y


            label_add_coord.set_position((new_x_add+0.5, new_y_add+0.5))
            label_add_coord.set_text(f"({new_x_add:.2f}, {new_y_add:.2f})")

            label_add.set_position((new_x_add/2+0.5, new_y_add/2+0.5))

            point_add.set_data([new_x_add], [new_y_add])

            add_xpoints[1] = new_x_add
            add_ypoints[1] = new_y_add

            line_add.set_data([add_xpoints], [add_ypoints])

        else:
            label_b_coord.set_position((new_x + 0.5, new_y + 0.5))
            label_b_coord.set_text(f"({new_x:.2f}, {new_y:.2f})")

            label_b.set_position((new_x/2+0.5, new_y/2+0.5))
            
            point_b.set_data([new_x], [new_y])

            b_xpoints[1] = new_x
            b_ypoints[1] = new_y

            line_b.set_data([b_xpoints], [b_ypoints])

            new_x_add = new_x + a_x
            new_y_add = new_y + a_y

            label_add_coord.set_position((new_x_add+0.5, new_y_add+0.5))
            label_add_coord.set_text(f"({new_x_add:.2f}, {new_y_add:.2f})")

            label_add.set_position((new_x_add/2+0.5, new_y_add/2+0.5))

            point_add.set_data([new_x_add], [new_y_add])

            add_xpoints[1] = new_x_add
            add_ypoints[1] = new_y_add

            line_add.set_data([add_xpoints], [add_ypoints])


        fig.canvas.draw_idle()

    def on_release(event):
        nonlocal is_dragging
        is_dragging = False
    
    fig.canvas.mpl_connect("button_press_event", on_pick)
    fig.canvas.mpl_connect("motion_notify_event", on_motion)
    fig.canvas.mpl_connect("button_release_event", on_release)

    plt.show()

if __name__ == "__main__":
    main()