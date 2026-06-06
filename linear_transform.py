import numpy as np
import matplotlib.pyplot as plt

def main():

    fig, ax = plt.subplots(figsize=(6, 6))
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    ax.grid(True)

    ax.locator_params(axis='both', nbins=5)

    triangle = np.array([
        [0, 2], 
        [-1, 0], 
        [1, 0], 
        [0, 2]
    ])

    scale = np.array([
        [2, 0], 
        [0, 0.5]
    ])

    reflectY = np.array([
        [1, 0],
        [0, -1]
    ])

    rad = np.radians(90)
    rotate = np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad), np.cos(rad)]
    ])

    scaled = triangle @ scale
    reflected = triangle @ reflectY
    rotated = triangle @ rotate



    ax.plot(triangle[:, 0], triangle[:, 1], marker = 'o')
    ax.plot(scaled[:, 0], scaled[:, 1])
    ax.plot(reflected[:, 0], reflected[:, 1])
    ax.plot(rotated[:, 0], rotated[:, 1])

    plt.show()

if __name__ == "__main__":
    main()