cmake_minimum_required(VERSION 3.0.2)
project(simple_lidar_navigation)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  sensor_msgs
  tf
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/wall_turn_controller.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY config launch rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
