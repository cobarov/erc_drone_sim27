import os
import random
import math
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    home_dir = os.path.expanduser('~')
    pkg_path = os.path.join(home_dir, 'erc_ws', 'src', 'erc_drone_sim')
    
    world_file = os.path.join(pkg_path, 'worlds', 'erc_drone.world')
    model_file = os.path.join(pkg_path, 'models', 'landing_target.sdf')
    
    # Gazebo'nun modellerimizi bulabilmesi için yolunu belirtiyoruz
    os.environ['GAZEBO_MODEL_PATH'] = os.path.join(pkg_path, 'models')
    
    # ÇÖZÜM BURADA: Gazebo'nun internette model arayıp yavaşlamasını engelliyoruz!
    os.environ['GAZEBO_MODEL_DATABASE_URI'] = ''

    # Rastgele konum hesaplama
    r = random.uniform(1.0, 2.5) 
    theta = random.uniform(0, 2 * math.pi)
    x_pos = str(r * math.cos(theta))
    y_pos = str(r * math.sin(theta))

    gazebo = ExecuteProcess(
        cmd=['gazebo', '--verbose', world_file, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'landing_target',
            '-file', model_file,
            '-x', x_pos,
            '-y', y_pos,
            '-z', '0.01'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        spawn_entity
    ])
