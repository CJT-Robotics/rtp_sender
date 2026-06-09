cmake_minimum_required(VERSION 3.0.2)
project(rtp_sender)

find_package(catkin REQUIRED COMPONENTS
  nodelet
  rospy
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)