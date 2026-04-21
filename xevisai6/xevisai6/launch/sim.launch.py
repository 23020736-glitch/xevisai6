import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg = get_package_share_directory('xevisai6')
    
    rviz_config_file = os.path.join(pkg, 'rviz2', 'my_config.rviz')
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    urdf_path = os.path.join(pkg, 'urdf', 'xevisai6.urdf')
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()
    
    robot_desc = robot_desc.replace('$(find xevisai6)', pkg)
    
    set_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=os.path.join(pkg, '..')
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_desc,
            'use_sim_time': True
        }],
        output='screen'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'verbose': 'true'}.items()
    )

    spawn = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='gazebo_ros',
                executable='spawn_entity.py',
                arguments=[
                    '-topic', 'robot_description',
                    '-entity', 'xevisai6'
                ],
                output='screen'
            )
        ]
    )

    joint_state = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['joint_state_broadcaster'],
                output='screen'
            )
        ]
    )

    diff = TimerAction(
        period=10.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['diff_drive_controller'],
                output='screen'
            )
        ]
    )

    arm = TimerAction(
        period=12.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['arm_controller'],
                output='screen'
            )
        ]
    )

    pris = TimerAction(
        period=14.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=['prismatic_controller'],
                output='screen'
            )
        ]
    )

 
    encoder_node = TimerAction(
        period=16.0,
        actions=[
            Node(
                package='xevisai6',
                executable='virtual_encoder.py', 
                name='virtual_encoder',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        set_model_path,
        rsp,
        rviz_node,
        gazebo,
        spawn,
        joint_state,
        diff,
        arm,
        pris,
        encoder_node
    ])
