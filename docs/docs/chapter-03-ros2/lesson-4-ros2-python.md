---
title: ROS 2 with Python (rclpy)
sidebar_label: ROS 2 with Python (rclpy)
sidebar_position: 4
description: Understanding ROS 2 development using Python and rclpy
---

# ROS 2 with Python (rclpy)

## Learning Objectives

- Understand the rclpy library and its role in ROS 2 Python development
- Implement ROS 2 nodes using Python
- Create publishers, subscribers, services, and actions in Python
- Understand the differences between rclpy and rospy
- Apply best practices for Python-based ROS 2 development

## Content

rclpy is the Python client library for ROS 2 that allows Python developers to create ROS 2 nodes, publishers, subscribers, services, and actions. It provides a Pythonic interface to the ROS 2 middleware and enables rapid prototyping and development.

### Understanding rclpy

rclpy is built on top of the ROS client library (rcl) and provides:

- **Node interface**: Create and manage ROS 2 nodes in Python
- **Communication primitives**: Publishers, subscribers, services, and actions
- **Parameter management**: Handle node parameters and configuration
- **Time utilities**: Manage ROS time and rates
- **Logging**: Integrate with ROS logging system

### Basic Node Structure

A typical ROS 2 Python node includes:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('node_name')
        # Initialize publishers, subscribers, etc.

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Creating Publishers

Creating a publisher in rclpy:

```python
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.get_clock().now().nanoseconds
        self.publisher.publish(msg)
```

### Creating Subscribers

Creating a subscriber in rclpy:

```python
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
```

### Creating Services

Creating a service server in rclpy:

```python
from example_interfaces.srv import AddTwoInts

class ServiceServerNode(Node):
    def __init__(self):
        super().__init__('service_server_node')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)
        
    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response
```

### Creating Clients

Creating a service client in rclpy:

```python
from example_interfaces.srv import AddTwoInts

class ServiceClientNode(Node):
    def __init__(self):
        super().__init__('service_client_node')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        
    def send_request(self, a, b):
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
            
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        self.future = self.cli.call_async(request)
```

### Parameters in rclpy

Handling parameters in rclpy:

```python
class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')
        self.declare_parameter('my_parameter', 'default_value')
        
    def get_parameter_value(self):
        my_param = self.get_parameter('my_parameter').value
        return my_param
```

### rclpy vs. rospy

Key differences between rclpy and rospy:

- **Architecture**: rclpy uses the new ROS 2 architecture with DDS middleware
- **Threading**: Better threading support in rclpy
- **Lifetime**: rclpy is actively maintained, rospy is in maintenance mode
- **Features**: rclpy supports ROS 2 features like Quality of Service, security, and multi-robot systems

### Best Practices

When developing with rclpy:

- **Use linters**: Apply Python linters like flake8 for code quality
- **Type hints**: Use type hints for better code documentation
- **Error handling**: Implement proper exception handling
- **Resource cleanup**: Always clean up resources when nodes are destroyed
- **Documentation**: Document your nodes and interfaces clearly

## Examples

A simple publisher-subscriber example in rclpy:

Publisher:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Key Takeaways

- rclpy is the Python client library for ROS 2
- It provides a Pythonic interface to ROS 2 communication primitives
- rclpy supports all ROS 2 communication patterns (topics, services, actions)
- Use proper resource cleanup and error handling when developing with rclpy
- Python provides fast prototyping capabilities for ROS 2 development