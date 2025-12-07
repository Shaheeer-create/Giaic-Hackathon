---
title: Nodes, Topics, and Messages
sidebar_position: 2
---

# Nodes, Topics, and Messages

## Learning Objectives

- Define nodes, topics, and messages in the ROS 2 context
- Understand how nodes communicate using topics and messages
- Identify the publisher-subscriber communication pattern
- Analyze the structure of ROS 2 messages
- Recognize best practices for designing ROS 2 communication

## Introduction

Nodes, topics, and messages form the fundamental communication architecture of ROS 2. This publisher-subscriber pattern enables modular robot software design where different components can be developed, tested, and maintained independently.

:::info
The publisher-subscriber pattern in ROS 2 allows for loose coupling between nodes, meaning publishers and subscribers don't need to know about each other's existence.
:::

### Nodes

A node in ROS 2 is a process that performs computation. Important characteristics of nodes include:

- **Process**: Each node is a separate process that can run on the same or different machines
- **Communication**: Nodes communicate with other nodes through topics, services, or actions
- **Identity**: Nodes have unique names within a ROS 2 domain
- **Lifecycle**: Nodes can have different states (unconfigured, inactive, active, finalized)

### Topics

Topics provide the infrastructure for the publisher-subscriber communication pattern:

- **Named buses**: Topics are named buses over which nodes exchange messages
- **One-to-many**: A publisher can send to many subscribers
- **Many-to-one**: Multiple publishers can publish to the same topic (though this is less common)
- **Decoupling**: Publishers and subscribers don't need to know about each other

### Messages

Messages are the data structures that are passed between nodes:

- **Definition**: Defined using .msg files with specific field types and names
- **Serialization**: Messages are automatically serialized and deserialized
- **Type Safety**: Each topic has a specific message type
- **Standard Types**: ROS 2 provides common message types (geometry_msgs, sensor_msgs, etc.)

:::note
Message types in ROS 2 ensure type safety across the communication system, preventing errors from mismatched data types.
:::

### Publisher-Subscriber Pattern

The publisher-subscriber pattern works as follows:

1. **Publishers** create and send messages to a topic
2. **Subscribers** receive messages from a topic
3. **Communication**: Publishers and subscribers are decoupled - they don't need to exist simultaneously

### Message Structure

ROS 2 messages have a well-defined structure:

```
# This is a comment
field_type field_name  # This is an inline comment

# Example message structure:
float64 x
float64 y
float64 z
string frame_id
```

### Quality of Service (QoS)

ROS 2 provides Quality of Service settings to control communication behavior:

- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Transient local vs. volatile
- **History**: Keep last N messages vs. all messages
- **Deadline**: Time limits for message delivery

:::tip
Choosing the appropriate QoS settings is crucial for ensuring your ROS 2 system behaves correctly under various conditions.
:::

### Practical Implementation

When implementing nodes:

- **Keep nodes focused**: Each node should have a single, well-defined purpose
- **Use appropriate QoS**: Match QoS settings to application requirements
- **Follow naming conventions**: Use consistent, descriptive names
- **Handle failures gracefully**: Implement proper error handling

## Examples

A robot navigation system might have:
- **Publisher**: A sensor node that publishes laser scan data to `/scan`
- **Subscriber**: A navigation node that subscribes to `/scan` to detect obstacles
- **Message**: `sensor_msgs/LaserScan` containing distance measurements

Multiple nodes can subscribe to the same sensor data:
- Navigation node for obstacle avoidance
- Mapping node for creating environment maps
- Safety node for emergency stopping

## Key Takeaways

- Nodes are computational processes that communicate via topics and messages
- Topics enable decoupled communication between nodes using publisher-subscriber pattern
- Messages are structured data with defined fields and types
- Quality of Service settings allow fine-tuning of communication behavior
- Good node design keeps each node focused on a single responsibility

In the next lesson, we'll explore services and actions in ROS 2 and how they differ from the topic-based communication model.