---
title: URDF for Humanoid Robots
sidebar_label: URDF for Humanoid Robots
sidebar_position: 6
description: Understanding Unified Robot Description Format for humanoid robots
---

# URDF for Humanoid Robots

## Learning Objectives

- Define Unified Robot Description Format (URDF) and its purpose
- Understand the structure and components of URDF files
- Create URDF descriptions for humanoid robots
- Analyze the relationship between URDF and robot kinematics
- Implement best practices for URDF design

## Content

Unified Robot Description Format (URDF) is an XML format used in ROS to describe robot models. For humanoid robots, URDF provides a way to define the robot's physical structure, joint characteristics, and visual representation, enabling simulation, planning, and control.

### What is URDF?

URDF (Unified Robot Description Format) is an XML format that describes a robot's:

- **Physical structure**: Links and joints that make up the robot
- **Visual representation**: How the robot appears in simulation and visualization
- **Collision properties**: How the robot interacts with its environment in simulation
- **Kinematic properties**: Joint limits, types, and ranges of motion
- **Inertial properties**: Mass, center of mass, and inertia for dynamics simulation

### URDF Structure

A URDF file contains:

- **Links**: Rigid bodies of the robot (e.g., torso, arms, legs)
- **Joints**: Connections between links (e.g., revolute, prismatic, fixed)
- **Materials**: Visual properties (color, texture)
- **Gazbo extensions**: Simulation-specific properties

### Links

Links represent rigid bodies in the robot:

```xml
<link name="link_name">
  <inertial>
    <mass value="1.0"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
  </inertial>
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.1 0.1 0.1"/>
    </geometry>
    <material name="blue">
      <color rgba="0 0 1 1"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="0.1 0.1 0.1"/>
    </geometry>
  </collision>
</link>
```

### Joints

Joints connect links and define their motion:

```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
</joint>
```

Joint types:
- **Fixed**: No motion allowed
- **Revolute**: Single axis rotation within limits
- **Continuous**: Single axis rotation without limits
- **Prismatic**: Single axis translation within limits
- **Planar**: Motion on a plane
- **Floating**: Free motion in 6DOF

### URDF for Humanoid Robots

Humanoid robots have specific requirements in their URDFs:

- **Symmetry**: Often mirrored limbs (left/right)
- **Bipedal structure**: Torso with two arms and two legs
- **Degrees of freedom**: Complex joint structures for human-like movement
- **Balance considerations**: Center of mass and stability factors

### Humanoid-specific Components

Typical humanoid URDF includes:

- **Torso**: Central body with head and attachment points
- **Arms**: Shoulder, elbow, and wrist joints
- **Legs**: Hip, knee, and ankle joints for bipedal locomotion
- **End effectors**: Hands with fingers for manipulation
- **Sensors**: IMUs in torso, cameras in head

### Kinematics and URDF

URDF defines the kinematic structure:

- **Forward kinematics**: Calculate end-effector position from joint angles
- **Inverse kinematics**: Calculate joint angles to achieve desired end-effector position
- **Kinematic chains**: Sequences of links and joints from base to end-effector

### Xacro for Complex URDFs

Xacro is an XML macro language that makes complex URDFs more manageable:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid_robot">
  <xacro:property name="M_PI" value="3.14159"/>
  
  <xacro:macro name="simple_arm" params="side prefix">
    <link name="${prefix}_upper_arm">
      <!-- link description -->
    </link>
    <joint name="${prefix}_shoulder_joint" type="revolute">
      <!-- joint description -->
    </joint>
  </xacro:macro>
  
  <xacro:simple_arm side="left" prefix="l"/>
  <xacro:simple_arm side="right" prefix="r"/>
</robot>
```

### URDF Tools and Visualization

ROS provides tools for working with URDF:

- **robot_state_publisher**: Publishes transforms based on joint states
- **joint_state_publisher**: Publishes joint state messages
- **RViz**: Visualizes robot models based on URDF
- **Gazebo**: Uses URDF for physics simulation

### Best Practices for Humanoid URDFs

When creating humanoid URDFs:

- **Use consistent naming**: Follow conventions for left/right, joint types
- **Include proper inertial properties**: Critical for simulation accuracy
- **Consider mass distribution**: Realistic inertial properties for stability
- **Use Xacro for complex robots**: Makes URDFs more maintainable
- **Test in simulation first**: Validate URDF before physical implementation
- **Document the structure**: Comment on the purpose of different parts

## Examples

A simplified URDF snippet for a humanoid's arm:

```xml
<link name="upper_arm">
  <visual>
    <geometry>
      <cylinder length="0.3" radius="0.05"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1.0"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.3" radius="0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.5"/>
    <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<joint name="shoulder_pitch" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.2 0.1 0.0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="50" velocity="2.0"/>
</joint>
```

## Key Takeaways

- URDF describes robot structure, kinematics, and visual properties
- Humanoid robots require complex URDFs with many degrees of freedom
- Xacro simplifies creation of complex, repetitive URDF structures
- Proper inertial properties are crucial for simulation accuracy
- URDF enables robot simulation, visualization, and kinematic calculations