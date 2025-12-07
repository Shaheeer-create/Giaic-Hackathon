---
title: What is ROS 2?
sidebar_position: 1
---

# What is ROS 2?

## Learning Objectives

- Define ROS 2 and its role in robotics development
- Understand the key differences between ROS 1 and ROS 2
- Identify the core concepts and architecture of ROS 2
- Recognize the benefits of using ROS 2 for robotics projects

## Introduction

Robot Operating System 2 (ROS 2) is not an actual operating system, but rather a flexible framework for writing robot software. It provides a collection of tools, libraries, and conventions that aim to simplify the development of complex and robust robot behavior across a wide variety of robot platforms.

:::info
ROS 2 serves as the "nervous system" for robots, enabling communication between different components and providing essential tools for development and debugging.
:::

### Understanding ROS 2

ROS 2 is the next generation of the Robot Operating System, designed to address the limitations of ROS 1 while maintaining the core principles that made ROS successful. It provides:

- A distributed computing framework
- Hardware abstraction
- Device drivers
- Libraries for implementing common robot functionality
- Tools for visualization, simulation, and testing
- Message-passing capabilities between processes

### Key Differences: ROS 1 vs. ROS 2

ROS 2 addresses several limitations of ROS 1:

- **Middleware**: ROS 2 uses DDS (Data Distribution Service) as its communication middleware
- **Quality of Service**: ROS 2 provides configurable Quality of Service policies for different application needs
- **Security**: First-class security support with authentication and encryption
- **Real-time support**: Better support for real-time systems
- **Cross-platform**: Improved support for Windows and macOS
- **Architecture**: More modular and maintainable architecture

### Core Concepts

ROS 2 is built around several core concepts:

- **Nodes**: Processes that perform computation; ROS 2 programs are composed of nodes
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication between nodes
- **Actions**: Asynchronous request/goal-based communication with feedback
- **Packages**: Collections of related resources that provide specific functionality

:::tip
Think of nodes as the individual components of a robot system (e.g., sensor processing, motion planning, control), and topics as the communication channels between these components.
:::

## Communication Architecture

ROS 2's communication is based on a distributed system architecture:

- **DDS Implementation**: Each ROS 2 node includes a DDS implementation
- **Peer-to-peer**: Nodes communicate directly without a central master
- **Language support**: Native support for C++, Python, and other languages

### Benefits of ROS 2

Using ROS 2 provides several advantages:

- **Community**: Large community with extensive documentation and packages
- **Tools**: Rich set of development tools for debugging and visualization
- **Flexibility**: Can run on a single machine or distributed across multiple machines
- **Modularity**: Easy to reuse and integrate existing components
- **Hardware abstraction**: Uniform interfaces for different hardware platforms

## Examples

A mobile manipulator robot might have separate nodes for:
- LIDAR processing
- Camera image processing
- Motion planning
- Arm control
- Navigation
- User interface

:::note
All these nodes communicate using ROS 2's messaging system, allowing for modular design and easy testing of individual components.
:::

## Key Takeaways

- ROS 2 is a framework for robot software development, not an actual operating system
- It uses DDS as its communication middleware, enabling better distributed communication
- Key concepts include nodes, topics, services, actions, and packages
- ROS 2 provides tools and infrastructure to build complex robotic systems efficiently

In the next lesson, we'll explore the fundamental communication patterns in ROS 2: nodes, topics, and messages.