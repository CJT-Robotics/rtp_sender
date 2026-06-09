# RTP Video Sender

## Overview

The **RTP Video Sender** is a ROS1 Noetic package designed for video streaming with ffmpeg.

It captures local video devices (V4L2) and utilizes FFmpeg inside a managed ROS launch environment to encode the stream into H.264 via RTP/UDP. The package supports multiple cameras simultaneously.

**Works perfectly with our [rtp receiver package](https://github.com/CJT-Robotics/rtp_receiver).**

## Requirements

Ensure FFmpeg with `libx264` encoding support is installed on your Debian/Ubuntu system:

```bash
sudo apt update
sudo apt install ffmpeg libavcodec-extra
```

The launch file relies on the standard ROS nodelet package to manage the standalone execution of external processes:

```bash
sudo apt install ros-noetic-nodelet
```

## Installation

Clone the repository into your Catkin workspace on the robot:

```bash
cd ~/catkin_ws/src
git clone git@github.com:CJT-Robotics/rtp_sender.git
```

Build the workspace:

```bash
cd ~/catkin_ws
catkin_make
```

Source your workspace:

```bash
source devel/setup.bash
```

## Usage

Start the ROS Master.

Launch the streaming pipeline using the default configuration:

```bash
roslaunch rtp_sender test.launch
```

## Configuration

### Multi-Camera Setup

You can stream from multiple hardware devices simultaneously by configuring the camera blocks inside the `test.launch` file, assigning unique UDP ports and video devices.

### Parameters

| Parameter     | Default       | Description                                             |
| ------------- | ------------- | ------------------------------------------------------- |
| `receiver_ip` | `127.0.0.1`   | IP address of the device receiving the stream |
| `cam1_dev`    | `/dev/video0` | V4L2 video device path for Camera 1                     |
| `cam1_port`   | `5000`        | Target UDP port for the Camera 1 RTP stream             |
| `cam1_fps`    | `20`          | Framerate                |
| `cam1_preset` | `good`        | Network quality preset (`good` or `poor`)               |

## Network Quality Presets

The launch file includes predefined bitrate limits:

### good (Standard Wi-Fi)

* Target bitrate: `750k`
* Maximum bitrate: `1M`
* Buffer size: `500k`

### poor (Degraded / Long-range Wi-Fi)

* Target bitrate: `350k`
* Maximum bitrate: `500k`
* Buffer size: `250k`

## Troubleshooting