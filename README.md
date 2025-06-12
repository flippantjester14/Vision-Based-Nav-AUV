# Vision-Based-Nav-AUV

This repository contains various Python utilities for controlling an Autonomous Underwater Vehicle (AUV) using camera feedback and MAVLink commands.

## Installation

1. Install the system dependencies on a Raspberry Pi running Linux:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pip python3-opencv python3-rospy
   ```
2. Install required Python packages:
   ```bash
   pip3 install pymavlink RPi.GPIO
   ```
3. Make sure ROS is installed and sourced in your environment. The scripts were
   developed with ROS Noetic but any recent ROS 1 distribution should work.

## Hardware Dependencies

- Raspberry Pi (tested on a Pi 4) with a GPIO-connected button for manual
  control.
- An autopilot running ArduSub that accepts MAVLink connections.
- Optional camera for the vision-based components.

## Software Dependencies

- ROS (tested with Noetic)
- `pymavlink`
- `OpenCV` (via `python3-opencv`)
- `RPi.GPIO` (for GPIO button handling)

## Usage

### 2wayswitch.py
`2wayswitch.py` listens for a button press on GPIO pin `27` to arm/disarm the
vehicle and perform a short preprogrammed maneuver.

Run it directly on the Raspberry Pi once the MAVLink connection is available:
```bash
python3 2wayswitch.py
```
The script waits for a long press on the button to arm the motors and start the
movement sequence. Press again to disarm.

### automove.py
`automove.py` is a simple ROS node that reads the `/custom_node/distance`
topic, logs the data to `auv_repositioning_data.csv` and publishes calculated
offsets on `/custom_node/distance_x` and `/custom_node/distance_y`.

Launch a ROS core and run the node with:
```bash
roscore &
python3 automove.py
```
Ensure other nodes publish the required `/custom_node/distance` topic.

