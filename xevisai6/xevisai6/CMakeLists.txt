cmake_minimum_required(VERSION 3.8)
project(xevisai6)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(gazebo_ros REQUIRED)
find_package(gazebo_ros2_control REQUIRED)
find_package(ros2_control REQUIRED)
find_package(ros2_controllers REQUIRED)

# Cài đặt toàn bộ các thư mục như trong ảnh của bạn
install(DIRECTORY launch urdf meshes config rviz2
  DESTINATION share/${PROJECT_NAME}
)

# Cài đặt file điều khiển trong thư mục scripts
install(PROGRAMS
  scripts/virtual_encoder.py
  scripts/teleop_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_export_dependencies(robot_state_publisher)
ament_package()
