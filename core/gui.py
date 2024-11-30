import matplotlib.pyplot as plt
import numpy as np

# Create figure and two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

def build_interface():
    # Set initial configurations for the interface
    ax1.set_xlim(-1500, 1500)
    ax1.set_ylim(-1500, 1500)
    ax1.set_xlabel('roll')
    ax1.set_ylabel('pitch')
    ax1.set_title('Pitch vs Roll')

    ax2.set_xlim(-1500, 1500)
    ax2.set_ylim(-1500, 1500)
    ax2.set_xlabel('yaw')
    ax2.set_ylabel('throttle')
    ax2.set_title('Yaw vs Throttle')

    plt.tight_layout()
    plt.show(block=False)

def parse_and_update_interface(msg):
    # Parse the byte message to extract pitch, roll, yaw, throttle
    pitch = int.from_bytes(msg[1:3], 'big')
    roll = int.from_bytes(msg[3:5], 'big')
    yaw = int.from_bytes(msg[5:7], 'big')
    throttle = int.from_bytes(msg[7:9], 'big')

    # Clear previous plots
    ax1.clear()
    ax2.clear()

    # Plot pitch vs roll
    ax1.plot([0, roll], [0, pitch], color='black')
    ax1.scatter([roll], [pitch], color='red')
    ax1.set_xlim(-1500, 1500)
    ax1.set_ylim(-1500, 1500)
    ax1.set_xlabel('roll')
    ax1.set_ylabel('pitch')
    ax1.set_title('Pitch vs Roll')

    # Plot yaw vs throttle
    ax2.plot([0, yaw], [0, throttle], color='black')
    ax2.scatter([yaw], [throttle], color='red')
    ax2.set_xlim(-1500, 1500)
    ax2.set_ylim(-1500, 1500)
    ax2.set_xlabel('yaw')
    ax2.set_ylabel('throttle')
    ax2.set_title('Yaw vs Throttle')

    # Draw updated plots
    plt.draw()
    plt.pause(0.01)
