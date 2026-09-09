# Minimal lidar navigation

This ROS1 Melodic package replaces the vendor move_base, AMCL, DWA, TEB,
waypoint, and TCP scheduling path with a small reactive controller.

    fresh /washing_machine_detected=true plus fresh /scan
                           |
                           v
                    APPROACH_MACHINE
                           |
                  front obstacle in /scan
                           |
                           v
                       TURN_RIGHT
                           |
                   measured right 90 degrees
                           |
                           +--------------> APPROACH_MACHINE

It is not a general navigation stack. It has no global planner, static-map
localization, costmap, waypoint list, network command interface, or autonomous
recovery behavior.

## Safety contract

- enabled defaults to false. While disabled, the node repeatedly publishes a
  zero Twist.
- The active controller has exactly two motion states: APPROACH_MACHINE and
  TURN_RIGHT. Disabled and fail-safe stopping are non-motion conditions.
- APPROACH_MACHINE sends forward velocity only when a fresh std_msgs/Bool
  message on /washing_machine_detected is true.
- TURN_RIGHT has priority when the forward lidar sector contains an obstacle
  within obstacle_distance. It turns using odometry yaw and stops if odometry
  is unavailable.
- The controller stops on stale scan data, stale machine detections, or stale
  odometry during a turn.
- Only one node may own /cmd_vel. Do not run this controller together with
  move_base, teleoperation, the vendor path tracker, or another velocity source
  unless a separately tested velocity multiplexer is in place.
- This package does not start a lidar driver or base driver. It cannot assume
  the physical robot, sensor model, serial port, or frame calibration.

## Build on the planned Melodic VM

Copy this source-only package into the Ubuntu 18.04 Melodic workspace after the
robot model is confirmed. From that workspace:

    catkin_make
    source devel/setup.bash

For offline inspection or simulation, start the two-state controller with:

    roslaunch simple_lidar_navigation simple_wall_turn.launch

That command leaves the controller disabled. A physical run requires an explicit
enabled:=true and separately validated /scan, /odom, /cmd_vel, TF, e-stop,
footprint, speed, and threshold values.

## Mapping visualization

mapping_visualization.launch starts only GMapping and RViz. A separate,
verified stack must already provide the selected scan topic and this TF chain:

    odom -> base_footprint -> lidar frame

The default mapping input is /scan_filtered, matching the original vendor
GMapping setup. RViz displays /map, /scan_filtered, /scan, /odom, and TF:

    roslaunch simple_lidar_navigation mapping_visualization.launch

This package does not include a saved map or a hardware-specific static laser
transform. Both must be measured and validated for the actual robot.
