#!/usr/bin/env python
"""A deliberately small, safety-gated lidar wall-turn controller.

The controller has three active states:

  DRIVE -> STOP -> TURN -> DRIVE

It drives straight, stops when an obstacle appears in the forward lidar sector,
waits for stop_duration, then turns by turn_angle using odometry yaw.
It does not use move_base, AMCL, a costmap, path following, or a network
scheduler. The node starts disabled and publishes only zero velocity until the
enabled parameter is explicitly set to true.
"""

from __future__ import division

import math

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion


STATE_DISABLED = "DISABLED"
STATE_DRIVE = "DRIVE"
STATE_STOP = "STOP"
STATE_TURN = "TURN"


def normalize_angle(angle):
    """Return an angle in the interval [-pi, pi)."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


class WallTurnController(object):
    """A minimal finite-state controller that requires fresh scan and odom."""

    def __init__(self):
        self.enabled = rospy.get_param("~enabled", False)
        self.front_half_angle = rospy.get_param("~front_half_angle", 0.35)
        self.obstacle_distance = rospy.get_param("~obstacle_distance", 0.45)
        self.drive_speed = rospy.get_param("~drive_speed", 0.12)
        self.turn_speed = rospy.get_param("~turn_speed", 0.35)
        self.turn_angle = abs(rospy.get_param("~turn_angle", math.pi / 2.0))
        self.turn_tolerance = rospy.get_param("~turn_tolerance", 0.04)
        self.turn_direction = 1 if rospy.get_param("~turn_direction", 1) >= 0 else -1
        self.stop_duration = rospy.Duration(rospy.get_param("~stop_duration", 0.5))
        self.odom_timeout = rospy.Duration(rospy.get_param("~odom_timeout", 0.5))
        self.scan_timeout = rospy.Duration(rospy.get_param("~scan_timeout", 0.5))

        self.state = STATE_DISABLED
        self.stop_until = None
        self.turn_start_yaw = None
        self.latest_front_distance = None
        self.last_scan_time = None
        self.current_yaw = None
        self.last_odom_time = None

        cmd_vel_topic = rospy.get_param("~cmd_vel_topic", "/cmd_vel")
        scan_topic = rospy.get_param("~scan_topic", "/scan")
        odom_topic = rospy.get_param("~odom_topic", "/odom")
        loop_hz = rospy.get_param("~loop_hz", 20.0)

        self.cmd_pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)
        rospy.Subscriber(scan_topic, LaserScan, self.scan_callback, queue_size=1)
        rospy.Subscriber(odom_topic, Odometry, self.odom_callback, queue_size=1)
        self.timer = rospy.Timer(rospy.Duration(1.0 / loop_hz), self.control_step)

        rospy.loginfo(
            "wall_turn_controller started disabled=%s scan=%s odom=%s cmd_vel=%s",
            self.enabled, scan_topic, odom_topic, cmd_vel_topic)

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    def publish_drive(self):
        command = Twist()
        command.linear.x = self.drive_speed
        self.cmd_pub.publish(command)

    def publish_turn(self):
        command = Twist()
        command.angular.z = self.turn_direction * self.turn_speed
        self.cmd_pub.publish(command)

    def set_state(self, next_state, reason):
        if self.state != next_state:
            rospy.loginfo("wall-turn state %s -> %s: %s", self.state, next_state, reason)
            self.state = next_state

    def scan_callback(self, scan):
        """Store the closest valid range in the configured forward sector."""
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

    def has_fresh_scan(self, now):
        return self.last_scan_time is not None and now - self.last_scan_time <= self.scan_timeout

    def has_fresh_odom(self, now):
        return (
            self.current_yaw is not None
            and self.last_odom_time is not None
            and now - self.last_odom_time <= self.odom_timeout
        )

    def obstacle_detected(self):
        return (
            self.latest_front_distance is not None
            and self.latest_front_distance <= self.obstacle_distance
        )

    def control_step(self, _event):
        now = rospy.Time.now()
        self.enabled = rospy.get_param("~enabled", self.enabled)

        if not self.enabled:
            self.set_state(STATE_DISABLED, "enabled=false")
            self.publish_stop()
            return

        if not self.has_fresh_scan(now):
            self.set_state(STATE_STOP, "waiting for a fresh lidar scan")
            self.publish_stop()
            return

        if self.state == STATE_DISABLED:
            self.set_state(STATE_DRIVE, "enabled=true with a fresh scan")

        if self.state == STATE_DRIVE:
            if self.obstacle_detected():
                self.stop_until = now + self.stop_duration
                self.set_state(
                    STATE_STOP,
                    "front obstacle %.3f m is within %.3f m" % (
                        self.latest_front_distance, self.obstacle_distance),
                )
                self.publish_stop()
            else:
                self.publish_drive()
            return

        if self.state == STATE_STOP:
            self.publish_stop()
            if self.stop_until is None:
                self.set_state(STATE_DRIVE, "fresh lidar scan resumed")
                return
            if now < self.stop_until:
                return
            if not self.has_fresh_odom(now):
                rospy.logwarn_throttle(
                    2.0,
                    "wall-turn remains stopped: fresh /odom is required for the turn",
                )
                return
            self.turn_start_yaw = self.current_yaw
            self.set_state(STATE_TURN, "stop duration elapsed; starting measured turn")
            return

        if self.state == STATE_TURN:
            if not self.has_fresh_odom(now):
                rospy.logwarn_throttle(
                    2.0,
                    "wall-turn remains stopped: odometry is stale during turn",
                )
                self.publish_stop()
                return
            turned = normalize_angle(self.current_yaw - self.turn_start_yaw)
            signed_progress = self.turn_direction * turned
            if signed_progress >= self.turn_angle - self.turn_tolerance:
                self.publish_stop()
                self.stop_until = None
                self.set_state(STATE_DRIVE, "turn target reached")
            else:
                self.publish_turn()

    def shutdown(self):
        self.publish_stop()


def main():
    rospy.init_node("wall_turn_controller")
    controller = WallTurnController()
    rospy.on_shutdown(controller.shutdown)
    rospy.spin()


if __name__ == "__main__":
    main()
