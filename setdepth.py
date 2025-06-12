from pymavlink import mavutil
from std_msgs.msg import Float32
import rospy

# Global variable to store depth value
depth_value = 0

def depth_callback(msg):
    global depth_value
    depth_value = msg.data

def send_rc_override_scaled(value):
    # Define the RC channel index (assuming it's channel 1, change it accordingly if needed)
    RC_CHANNEL = 1

    # Connect to the autopilot (change the connection string as per your setup)
    master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    # Scale the value from -2 to 2 to 1000 to 2000 PWM
    pwm_value = int((value + 2) * 500) + 1000

    # Clamp PWM value to 1000-2000 range
    pwm_value = max(1000, min(pwm_value, 2000))

    # Set PWM values for all channels
    # Channel 1 is overridden, other channels are set to 1500 PWM
    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,
        pwm_value,   # Channel 1 override value
        1500,        # Channel 2 override value
        1500,        # Channel 3 override value
        1500,        # Channel 4 override value
        1500,        # Channel 5 override value
        1500,        # Channel 6 override value
        1500,        # Channel 7 override value
        1500         # Channel 8 override value
    )

    # Close the MAVLink connection
    master.close()

if __name__ == "__main__":
    try:
        # Initialize the ROS node
        rospy.init_node('set_depth_node', anonymous=True)

        # Subscribe to the depth topic
        rospy.Subscriber('/custom_node/z_pixel', Float32, depth_callback)

        # Example loop to continuously send RC override commands
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            # Send RC override command with the scaled depth value
            send_rc_override_scaled(depth_value)
            rate.sleep()

    except rospy.ROSInterruptException:
        print("ROS node terminated")

