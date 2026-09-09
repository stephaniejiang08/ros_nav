#!/usr/bin/env python
"""A two-state, safety-gated lidar and vision controller.

Active states:

  APPROACH_MACHINE: a fresh vision Bool reports a washing machine, so drive.
  TURN_RIGHT: a front lidar obstacle is present, so turn right by 90 degrees.

The obstacle state has priority over the machine state. The controller begins
disabled and sends zero velocity unless all required input is fresh.
"""

from __future__ import division

import math

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from tf.transformations import euler_from_quaternion


STATE_DISABLED = "DISABLED"
STATE_APPROACH_MACHINE = "APPROACH_MACHINE"
STATE_TURN_RIGHT = "TURN_RIGHT"


def normalize_angle(angle):
    """Return an angle in the interval [-pi, pi)."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class MachineStateController(object):
    """Minimal two-active-state controller with fail-safe zero velocity."""

    def __init__(self):
        self.enabled = rospy.get_param("~enabled", False)
        self.front_half_angle = rospy.get_param("~front_half_angle", 0.35)
        self.obstacle_distance = rospy.get_param("~obstacle_distance", 0.45)
        self.drive_speed = rospy.get_param("~drive_speed", 0.12)
        self.turn_speed = abs(rospy.get_param("~turn_speed", 0.35))
        self.turn_angle = abs(rospy.get_param("~turn_angle", math.pi / 2.0))
        self.turn_tolerance = rospy.get_param("~turn_tolerance", 0.04)
        self.scan_timeout = rospy.Duration(rospy.get_param("~scan_timeout", 0.5))
        self.odom_timeout = rospy.Duration(rospy.get_param("~odom_timeout", 0.5))
        self.machine_timeout = rospy.Duration(rospy.get_param("~machine_timeout", 0.5))

        self.state = STATE_DISABLED
        self.latest_front_distance = None
        self.last_scan_time = None
        self.machine_visible = False
        self.last_machine_time = None
        self.current_yaw = None
        self.last_odom_time = None
        self.turn_start_yaw = None

        cmd_vel_topic = rospy.get_param("~cmd_vel_topic", "/cmd_vel")
        scan_topic = rospy.get_param("~scan_topic", "/scan")
        odom_topic = rospy.get_param("~odom_topic", "/odom")
        machine_topic = rospy.get_param(
            "~washing_machine_detected_topic", "/washing_machine_detected")
        loop_hz = rospy.get_param("~loop_hz", 20.0)

        self.cmd_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(scan_topic, LaserScan, self.scan_callback, queue_size=1)
        rospy.Subscriber(odom_topic, Odometry, self.odom_callback, queue_size=1)
        rospy.Subscriber(machine_topic, Bool, self.machine_callback, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(1.0 / loop_hz), self.control_step)

        rospy.loginfo(
            "machine controller started disabled=%s scan=%s odom=%s machine=%s "
            "cmd_vel=%s",
            self.enabled, scan_topic, odom_topic, machine_topic, cmd_vel_topic)

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    def publish_drive(self):
        command = Twist()
        command.linear.x = self.drive_speed
        self.cmd_pub.publish(command)

    def publish_turn_right(self):
        command = Twist()
        command.angular.z = -self.turn_speed
        self.cmd_pub.publish(command)

    def set_state(self, next_state, reason):
        if self.state != next_state:
            rospy.loginfo("machine state %s -> %s: %s", self.state, next_state, reason)
            self.state = next_state

    def scan_callback(self, scan):
        """Store the closest valid point in the configured forward sector."""
        closest = None
        for index, distance in enumerate(scan.ranges):
            angle = scan.angle_min + index * scan.angle_increment
            valid = not math.isinf(distance) and not math.isnan(distance)
            within_sensor_range = scan.range_min <= distance <= scan.range_max
            if valid and within_sensor_range and abs(angle) <= self.front_half_angle:
                if closest is None or distance < closest:
                    closest = distance
        self.latest_front_distance = closest
        self.last_scan_time = rospy.Time.now()

    def odom_callback(self, odom):
        orientation = odom.pose.pose.orientation
        quaternion = [orientation.x, orientation.y, orientation.z, orientation.w]
        self.current_yaw = euler_from_quaternion(quaternion)[2]
        self.last_odom_time = rospy.Time.now()

    def machine_callback(self, detected):
        self.machine_visible = detected.data
        self.last_machine_time = rospy.Time.now()

    def has_fresh_scan(self, now):
        return self.last_scan_time is not None and now - self.last_scan_time <= self.scan_timeout

    def has_fresh_odom(self, now):
        return (
            self.current_yaw is not None
            and self.last_odom_time is not None
            and now - self.last_odom_time <= self.odom_timeout
        )

    def has_fresh_machine_detection(self, now):
        return (
            self.last_machine_time is not None
            and now - self.last_machine_time <= self.machine_timeout
        )

    def obstacle_detected(self):
        return (
            self.latest_front_distance is not None
            and self.latest_front_distance <= self.obstacle_distance
        )

    def start_right_turn(self, now):
        if not self.has_fresh_odom(now):
            rospy.logwarn_throttle(
                2.0,
                "machine controller stopped: fresh /odom is required for a right turn",
            )
            self.publish_stop()
            return False
        self.turn_start_yaw = self.current_yaw
        self.set_state(STATE_TURN_RIGHT, "front obstacle takes priority")
        self.publish_stop()
        return True

    def control_step(self, _event):
        now = rospy.Time.now()
        self.enabled = rospy.get_param("~enabled", self.enabled)

        if not self.enabled:
            self.set_state(STATE_DISABLED, "enabled=false")
            self.publish_stop()
            return

        if not self.has_fresh_scan(now):
            rospy.logwarn_throttle(
                2.0, "machine controller stopped: waiting for a fresh lidar scan")
            self.publish_stop()
            return

        if self.state == STATE_DISABLED:
            self.set_state(STATE_APPROACH_MACHINE, "enabled=true with fresh lidar")

        if self.state == STATE_APPROACH_MACHINE:
            if self.obstacle_detected():
                self.start_right_turn(now)
                return
            if self.has_fresh_machine_detection(now) and self.machine_visible:
                self.publish_drive()
            else:
                self.publish_stop()
            return

        if self.state == STATE_TURN_RIGHT:
            if not self.has_fresh_odom(now):
                rospy.logwarn_throttle(
                    2.0,
                    "machine controller stopped: odometry is stale during right turn",
                )
                self.publish_stop()
                return

            turned_right = -normalize_angle(self.current_yaw - self.turn_start_yaw)
            if turned_right >= self.turn_angle - self.turn_tolerance:
                self.publish_stop()
                self.set_state(STATE_APPROACH_MACHINE, "right-turn target reached")
            else:
                self.publish_turn_right()

    def shutdown(self):
        self.publish_stop()


def main():
    rospy.init_node("machine_state_controller")
    controller = MachineStateController()
    rospy.on_shutdown(controller.shutdown)
    rospy.spin()


if __name__ == "__main__":
    main()
