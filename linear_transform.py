import numpy as np
import matplotlib.pyplot as plt

def main():

    fig, ax = plt.subplots(figsize=(6, 6))
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    ax.grid(True)

    ax.locator_params(axis='both', nbins=5)

    is_dragging = False

    a_initial_x = -1
    a_initial_y = 1

    b_initial_x = 2
    b_initial_y = 2

    point_a, = ax.plot(a_initial_x, a_initial_y, marker="o", color="firebrick", markersize=10, picker=True) 
    
    label_a = ax.text(a_initial_x+0.5, a_initial_y+0.5, f"({a_initial_x:.2f}, {a_initial_y:.2f})", fontsize=10, color="firebrick")

    point_b, = ax.plot(b_initial_x, b_initial_y, marker="o", color="blue", markersize=10, picker=True) 
    
    label_b = ax.text(b_initial_x+0.5, b_initial_y+0.5, f"({b_initial_x:.2f}, {b_initial_y:.2f})", fontsize=10, color="blue")

    a_xpoints = [0, a_initial_x]
    a_ypoints = [0, a_initial_y]

    b_xpoints = [0, b_initial_x]
    b_ypoints = [0, b_initial_y]

    line_a, = ax.plot(a_xpoints, a_ypoints, color="firebrick", linestyle="-")
    line_b, = ax.plot(b_xpoints, b_ypoints, color="blue", linestyle="-")

    def on_pick(event):
        if event.inaxes != ax: 
            return
        
        nonlocal is_dragging
        ax, ay = point_a.get_data()
        bx, by = point_b.get_data()

        if abs(event.xdata - ax[0]) < 0.5 and abs(event.ydata - ay[0]  < 0.5):
            is_dragging = "A"
        elif abs(event.xdata - bx[0]) < 0.5 and abs(event.ydata - by[0]  < 0.5):
            is_dragging = "B"
    
    def on_motion(event):
        if not is_dragging or event.inaxes != ax:
            return
        
        new_x = event.xdata
        new_y = event.ydata

        if (is_dragging == "A"):
            label_a.set_position((new_x + 0.5, new_y + 0.5))
            label_a.set_text(f"({new_x:.2f}, {new_y:.2f})")
            
            point_a.set_data([event.xdata], [event.ydata])

            a_xpoints[1] = new_x
            a_ypoints[1] = new_y

            line_a.set_data([a_xpoints], [a_ypoints])

        else:
            label_b.set_position((new_x + 0.5, new_y + 0.5))
            label_b.set_text(f"({new_x:.2f}, {new_y:.2f})")
            
            point_b.set_data([event.xdata], [event.ydata])

            b_xpoints[1] = new_x
            b_ypoints[1] = new_y

            line_b.set_data([b_xpoints], [b_ypoints])


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