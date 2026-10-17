import os
import random
import math
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    home_dir = os.path.expanduser('~')
    pkg_path = os.path.join(home_dir, 'erc_ws', 'src', 'erc_drone_sim')
    
    world_file = os.path.join(pkg_path, 'worlds', 'erc_drone.world')
    target_file = os.path.join(pkg_path, 'models', 'landing_target.sdf')
    
    # Get the install path for the s500 package
    s500_pkg_share = get_package_share_directory('itu_s500_description')
    
    # CRITICAL FIX: Tell Gazebo where to find the ROS 2 package meshes
    # We add the parent directory of the package share to the Gazebo model path
    gazebo_models_path = os.path.join(home_dir, 'erc_ws', 'install', 'itu_s500_description', 'share')
    
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = os.path.join(pkg_path, 'models') + ':' + gazebo_models_path + ':' + os.environ['GAZEBO_MODEL_PATH']
    else:
        os.environ['GAZEBO_MODEL_PATH'] = os.path.join(pkg_path, 'models') + ':' + gazebo_models_path

    os.environ['GAZEBO_MODEL_DATABASE_URI'] = ''

    r = random.uniform(1.0, 2.5) 
    theta = random.uniform(0, 2 * math.pi)
    x_pos = str(r * math.cos(theta))
    y_pos = str(r * math.sin(theta))

    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_file, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    spawn_target = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'landing_target', '-file', target_file, '-x', x_pos, '-y', y_pos, '-z', '0.01'],
        output='screen'
    )

    urdf_file = os.path.join(s500_pkg_share, 'urdf', 's500.itu.urdf')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_file])}]
    )

    spawn_s500 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'itu_s500', '-topic', 'robot_description', '-x', '0', '-y', '0', '-z', '0.2'],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_target,
        robot_state_publisher_node,
        spawn_s500
    ])
