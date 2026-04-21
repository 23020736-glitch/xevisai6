#  Xevisai6 ROS2 Simulation Guide

##  Giới thiệu

Package `xevisai6` dùng để mô phỏng và điều khiển robot vi sai trong ROS 2:

* Teleop bàn phím
* Mô phỏng Gazebo
* Sử dụng `ros2_controllers`

---

##  Cài ros2_controllers

```bash
sudo apt update
sudo apt install ros-humble-ros2-controllers
```

---

##  Cài dependency

cd ~/ros2_ws && rosdep install --from-paths src --ignore-src -r -y

##  Tạo workspace & thêm package

cd ~ && mkdir -p ros2_ws/src && cp -r ~/Downloads/xevisai6 ~/ros2_ws/src/


##  Build

cd ~/ros2_ws && colcon build --symlink-install --packages-select xevisai6


##  Source
source ~/ros2_ws/install/setup.bash

##  Chạy teleop

cd ~/ros2_ws && source install/setup.bash && ros2 run xevisai6 teleop_node.py


Nếu lỗi quyền:

```bash
chmod +x ~/ros2_ws/src/xevisai6/xevisai6/teleop_node.py
```

---

##  Chạy Gazebo

cd ~/ros2_ws && rm -rf build/ install/ log/ && colcon build --symlink-install --packages-select xevisai6 && source install/setup.bash && ros2 launch xevisai6 sim.launch.py




