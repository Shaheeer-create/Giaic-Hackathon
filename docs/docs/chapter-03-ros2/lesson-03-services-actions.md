---
title: Services and Actions
sidebar_position: 3
---

# Services and Actions

## Learning Objectives

- Define services and actions in the ROS 2 context
- Understand the differences between topics, services, and actions
- Implement service clients and servers
- Implement action clients and servers
- Choose the appropriate communication method for different scenarios

## Introduction

While topics provide asynchronous, decoupled communication, services and actions offer synchronous and goal-oriented communication patterns in ROS 2. Understanding when to use each pattern is crucial for effective robot software design.

:::info
ROS 2 offers three primary communication patterns: topics (asynchronous), services (synchronous request/response), and actions (goal-oriented with feedback).
:::

### Services

Services provide synchronous request/response communication:

- **Synchronous**: Client sends request and waits for response
- **One-to-one**: One client communicates with one server at a time
- **Request-Response**: Each request gets exactly one response
- **Blocking**: Client blocks until response is received

#### Service Structure

A service consists of:
- **Request**: Message sent from client to server
- **Response**: Message sent from server to client
- **Definition**: Defined in .srv files with both request and response parts

Example service definition (.srv file):
```
# Request part (before ---)
string name
int32 age
---
# Response part (after ---)
bool success
string message
```

### Actions

Actions provide goal-based communication with feedback:

- **Goal-oriented**: Client sends a goal to server to perform a long-running task
- **Feedback**: Server provides continuous feedback during task execution
- **Result**: Server sends final result when task completes
- **Cancellation**: Clients can cancel goals in progress

:::note
Actions are particularly useful for long-running tasks that need monitoring or can be cancelled.
:::

#### Action Structure

An action consists of:
- **Goal**: Request to initiate a long-running task
- **Feedback**: Continuous updates during task execution
- **Result**: Final outcome when task completes
- **Definition**: Defined in .action files with goal, feedback, and result parts

Example action definition (.action file):
```
# Goal
int32 goal_value
---
# Result
int32 result_value
bool success
---
# Feedback
int32 current_value
float32 percent_complete
```

### When to Use Each Communication Pattern

- **Topics**: Use for continuous data streams, sensor data, or broadcasting information
  - Examples: Camera images, laser scans, robot pose
  - Characteristics: Asynchronous, one-to-many, no response required

- **Services**: Use for simple queries, configuration changes, or tasks with clear outcomes
  - Examples: Saving map, changing parameters, requesting transform
  - Characteristics: Synchronous, request-response, blocking

- **Actions**: Use for long-running tasks that need monitoring or cancellation
  - Examples: Navigation to goal, trajectory execution, calibration procedures
  - Characteristics: Goal-oriented, provides feedback, cancellable

### Service Implementation

Service server:
1. Creates service server for a specific service type
2. Registers callback function to handle requests
3. Waits for requests and provides responses

Service client:
1. Creates client for a specific service type
2. Sends request to server
3. Waits for and processes response

### Action Implementation

Action server:
1. Creates action server for specific action type
2. Registers callbacks for accepting goals, executing goals, and handling cancellation
3. Provides continuous feedback and final result

Action client:
1. Creates action client for specific action type
2. Sends goal to server
3. Monitors feedback and retrieves final result

:::tip
Choose communication patterns based on the specific requirements of your use case: topics for streaming data, services for queries, and actions for long-running tasks.
:::

### Advantages and Considerations

**Services advantages:**
- Simple request/response pattern
- Good for configuration and simple queries
- Built-in error handling

**Services considerations:**
- Blocking nature can stall client
- Not suitable for long-running tasks

**Actions advantages:**
- Perfect for long-running tasks
- Provides feedback on progress
- Supports cancellation
- Non-blocking communication

**Actions considerations:**
- More complex implementation than services
- Overhead for simple tasks

## Examples

A robot navigation system might use:
- **Topics**: Publish robot position, sensor data
- **Services**: Save current map, clear costmap, switch navigation modes
- **Actions**: Move robot to goal location (with feedback on progress)

## Key Takeaways

- Services provide synchronous request/response communication
- Actions provide goal-oriented communication with feedback and cancellation
- Choose communication patterns based on the specific requirements of your use case
- Topics for continuous data, services for queries, actions for long-running tasks

In the next chapter, we'll explore robot simulation environments and their role in developing and testing robotics systems.