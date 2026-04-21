#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32
import math

class VirtualEncoder(Node):
    def __init__(self):
        super().__init__('virtual_encoder')
        
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
            
        self.pub_left = self.create_publisher(Int32, '/left_encoder_ticks', 10)
        self.pub_right = self.create_publisher(Int32, '/right_encoder_ticks', 10)

        # So xung cua Encoder tren 1 vong quay (Thay doi neu can)
        self.PPR = 330 

    def listener_callback(self, msg):
        try:
            left_idx = msg.name.index('left_joint')
            right_idx = msg.name.index('right_joint')

            left_rad = msg.position[left_idx]
            right_rad = msg.position[right_idx]

            left_ticks = int((left_rad / (2 * math.pi)) * self.PPR)
            right_ticks = int((right_rad / (2 * math.pi)) * self.PPR)

            left_msg = Int32()
            left_msg.data = left_ticks
            self.pub_left.publish(left_msg)

            right_msg = Int32()
            right_msg.data = right_ticks
            self.pub_right.publish(right_msg)

            self.get_logger().info(f'Ticks - Trai: {left_ticks} | Phai: {right_ticks}')
            
        except ValueError:
            pass

def main(args=None):
    rclpy.init(args=args)
    virtual_encoder = VirtualEncoder()
    rclpy.spin(virtual_encoder)
    virtual_encoder.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
