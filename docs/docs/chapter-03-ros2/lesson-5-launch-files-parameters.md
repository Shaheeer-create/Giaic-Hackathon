---
title: Launch Files and Parameters
sidebar_label: Launch Files and Parameters
sidebar_position: 5
description: Understanding ROS 2 launch files and parameter management
---

# Launch Files and Parameters

## Learning Objectives

- Understand the purpose and structure of ROS 2 launch files
- Create launch files using Python and XML
- Manage parameters in ROS 2 systems
- Configure nodes using parameter files
- Implement best practices for launch file design

## Content

Launch files and parameters are essential components of ROS 2 systems that allow for systematic configuration and launching of multiple nodes. They provide a way to run complex robotic systems with consistent configurations without hardcoding values.

### Launch Files Overview

Launch files in ROS 2 provide:

- **Multiple node launching**: Start multiple nodes with a single command
- **Configuration**: Set parameters, remap topics, and configure nodes
- **Organization**: Group related nodes into logical applications
- **Flexibility**: Create different configurations for different scenarios

### Launch File Types

ROS 2 supports multiple launch file formats:

- **Python launch files**: More flexible, support complex logic
- **XML launch files**: Simpler, more declarative (currently in development)
- **YAML launch files**: Declarative format for simple configurations

### Python Launch Files

Python launch files use the launch package:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='package_name',
            executable='executable_name',
            name='node_name',
            parameters=[
                {'param1': 'value1'},
                {'param2': 42},
            ],
            remappings=[
                ('/original_topic', '/new_topic'),
            ]
        )
    ])
```

### Launch File Elements

Launch files can include various elements:

- **Nodes**: ROS 2 nodes to launch
- **Parameters**: Configuration values for nodes
- **Conditions**: Conditional launching based on arguments
- **Arguments**: Input parameters for launch files
- **Actions**: Other launch actions (timers, event handlers)

### Parameters in ROS 2

Parameters in ROS 2 provide:

- **Configuration**: Runtime configuration of nodes
- **Dynamic reconfiguration**: Change parameters while nodes are running
- **Hierarchical organization**: Organize parameters in a tree structure
- **Type safety**: Strong typing of parameter values

### Parameter Sources

Parameters can come from multiple sources:

- **Built-in defaults**: Parameters defined in node code
- **Launch files**: Parameters specified in launch files
- **YAML files**: External parameter files
- **Command line**: Parameters specified at runtime
- **Parameter servers**: Centralized parameter management

### Parameter YAML Files

Parameters can be organized in YAML files:

```yaml
node_name:
  ros__parameters:
    param1: value1
    param2: 42
    nested:
      param3: 3.14
      param4: true
```

### Working with Parameters in Code

Parameters in node code:

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        
        # Declare parameters with defaults
        self.declare_parameter('my_param', 'default_value')
        self.declare_parameter('another_param', 10)
        
        # Get parameter values
        my_param = self.get_parameter('my_param').value
        another_param = self.get_parameter('another_param').value
        
        # Parameter callbacks
        self.add_on_set_parameters_callback(self.parameters_callback)
        
    def parameters_callback(self, params):
        for param in params:
            if param.name == 'my_param' and param.type_ == Parameter.Type.STRING:
                self.get_logger().info(f'Parameter {param.name} set to {param.value}')
        return SetParametersResult(successful=True)
```

### Launch File Arguments

Launch files can accept arguments:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    param_config_arg = DeclareLaunchArgument(
        'param_config',
        default_value='default_config.yaml',
        description='Path to parameter configuration file'
    )
    
    # Use launch configuration
    params_file = LaunchConfiguration('param_config')
    
    return LaunchDescription([
        param_config_arg,
        Node(
            package='package_name',
            executable='node_name',
            name='node_name',
            parameters=[params_file]
        )
    ])
```

### Best Practices

When designing launch files and parameters:

- **Modularity**: Break large launch files into smaller, reusable components
- **Documentation**: Document all launch arguments and parameters
- **Defaults**: Provide sensible default values
- **Validation**: Validate parameter values in your nodes
- **Organization**: Group related parameters logically
- **Consistency**: Use consistent naming conventions

## Examples

A launch file for a basic navigation system:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )
    
    return LaunchDescription([
        use_sim_time,
        
        # Laser scanner node
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            parameters=[
                {'channel_type': 'serial'},
                {'serial_port': '/dev/ttyUSB0'},
                {'frame_id': 'laser_link'},
                {'inverted': False},
                {'angle_compensate': True},
            ],
            output='screen'
        ),
        
        # Navigation node
        Node(
            package='navigation_package',
            executable='nav_node',
            name='nav_node',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'map_resolution': 0.05},
                {'planner_frequency': 1.0},
            ],
            remappings=[
                ('/scan', '/sllidar_node/scan'),
            ],
            output='screen'
        )
    ])
```

## Key Takeaways

- Launch files enable coordinated startup of multiple nodes
- Parameters allow configuration without recompilation
- YAML files provide a clean way to organize parameter configurations
- Python launch files offer flexibility for complex system configurations
- Proper parameter management is essential for maintainable ROS 2 systems