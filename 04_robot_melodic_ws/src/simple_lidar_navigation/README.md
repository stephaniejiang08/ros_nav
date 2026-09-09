# Minimal lidar navigation

This ROS1 Melodic package replaces the vendor move_base, AMCL, DWA, TEB,
waypoint, and TCP scheduling path with a small reactive controller.

    fresh /scan plus fresh /odom
              |
              v
    DRIVE -> obstacle -> STOP -> measured 90-degree TURN -> DRIVE

It is not a general navigation stack. It has no global planner, static-map
localization, costmap, waypoint list, network command interface, or autonomous
recovery behavior.

## Safety contract

- enabled defaults to false. While disabled, the node repeatedly publishes a
  zero Twist.
- The controller stops on stale scan data or stale odometry.
- Turning uses odometry yaw. It stays stopped instead of time-estimating a
  90-degree turn when odometry is unavailable.
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

For offline inspection or simulation, start the controller with:

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
