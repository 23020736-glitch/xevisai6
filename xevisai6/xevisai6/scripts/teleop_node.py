#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray  # Sửa lại kiểu dữ liệu cho đúng Controller
import sys, tty, termios, threading

# Giới hạn khớp
ARM_LOWER, ARM_UPPER = 0.0, 2.0
PRIS_LOWER, PRIS_UPPER = 0.0, 0.11
ARM_STEP, PRIS_STEP = 0.1, 0.01

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        
        # Publisher cho xe chạy
        self.cmd_pub = self.create_publisher(Twist, '/diff_drive_controller/cmd_vel_unstamped', 10)
        
        # Publisher cho tay máy (Sửa thành Float64MultiArray để khớp với PositionController)
        self.arm_pub = self.create_publisher(Float64MultiArray, '/arm_controller/commands', 10)
        self.pris_pub = self.create_publisher(Float64MultiArray, '/prismatic_controller/commands', 10)
        
        self.arm_pos = 0.0
        self.pris_pos = 0.0

    def _send_command(self, publisher, position):
        msg = Float64MultiArray()
        msg.data = [float(position)]
        publisher.publish(msg)

    def update_state(self, key):
        twist = Twist()
        if key == 'w': twist.linear.x = 0.5
        elif key == 's': twist.linear.x = -0.5
        elif key == 'a': twist.angular.z = 1.0
        elif key == 'd': twist.angular.z = -1.0
        
        # Điều khiển khớp xoay (Arm)
        elif key == 'u':
            self.arm_pos = min(self.arm_pos + ARM_STEP, ARM_UPPER)
            self._send_command(self.arm_pub, self.arm_pos)
        elif key == 'o':
            self.arm_pos = max(self.arm_pos - ARM_STEP, ARM_LOWER)
            self._send_command(self.arm_pub, self.arm_pos)
            
        # Điều khiển khớp trượt (Prismatic)
        elif key == 'j':
            self.pris_pos = min(self.pris_pos + PRIS_STEP, PRIS_UPPER)
            self._send_command(self.pris_pub, self.pris_pos)
        elif key == 'l':
            self.pris_pos = max(self.pris_pos - PRIS_STEP, PRIS_LOWER)
            self._send_command(self.pris_pub, self.pris_pos)
            
        elif key == ' ': # Dừng xe
            twist = Twist()
            
        self.cmd_pub.publish(twist)

def main():
    rclpy.init()
    node = KeyboardTeleop()
    settings = termios.tcgetattr(sys.stdin)
    
    print("-" * 30)
    print("ROS 2 xevisai6 Teleop")
    print("Xe: W (Tien), S (Lui), A (Trai), D (Phai)")
    print("Tay may: U/O (Xoay), J/L (Nang/Ha)")
    print("Space: Dung xe | Ctrl+C: Thoat")
    print("-" * 30)

    def get_key():
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    thread.start()

    try:
        while rclpy.ok():
            key = get_key()
            if key == '\x03': break
            node.update_state(key)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
