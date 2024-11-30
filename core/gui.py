import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

# Matplotlib Styling
style.use('fivethirtyeight')

# Create Figure and Axes for the Graphs
fig, (ax1, ax2) = plt.subplots(2, 1)

# Placeholder data for the graphs
x_data = []
y_pitch = []
y_roll = []
y_yaw = []
y_throttle = []

def animate(i, msg):
    # Extract values for graphing from the message
    pitch = msg['pitch']
    roll = msg['roll']
    yaw = msg['yaw']
    throttle = msg['throttle']

    # Update data lists
    x_data.append(len(x_data))
    y_pitch.append(pitch)
    y_roll.append(roll)
    y_yaw.append(yaw)
    y_throttle.append(throttle)

    # Limit lists to the last 20 points
    x_data_trimmed = x_data[-20:]
    y_pitch_trimmed = y_pitch[-20:]
    y_roll_trimmed = y_roll[-20:]
    y_yaw_trimmed = y_yaw[-20:]
    y_throttle_trimmed = y_throttle[-20:]

    # Clear and plot on ax1 (Pitch vs Roll)
    ax1.clear()
    ax1.plot(x_data_trimmed, y_pitch_trimmed, label='Pitch')
    ax1.plot(x_data_trimmed, y_roll_trimmed, label='Roll', color='orange')
    ax1.set_title('Pitch vs Roll over Time')
    ax1.set_ylabel('Value')
    ax1.legend()

    # Clear and plot on ax2 (Yaw vs Throttle)
    ax2.clear()
    ax2.plot(x_data_trimmed, y_yaw_trimmed, label='Yaw', color='green')
    ax2.plot(x_data_trimmed, y_throttle_trimmed, label='Throttle', color='red')
    ax2.set_title('Yaw vs Throttle over Time')
    ax2.set_ylabel('Value')
    ax2.set_xlabel('Time')
    ax2.legend()

# Example function to draw graphs with given message
def draw_graphs(msg):
    ani = animation.FuncAnimation(fig, animate, fargs=(msg,), interval=100, repeat=False)
    plt.tight_layout()
    plt.show()

# Example usage
msg = {'pitch': 0.5, 'roll': 0.3, 'yaw': 0.1, 'throttle': 0.7}
draw_graphs(msg)
