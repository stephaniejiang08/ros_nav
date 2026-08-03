# Ubuntu 18.04 / ROS Melodic Robot Compatibility VM Plan

Status: `PLAN_ONLY`. This file must not be executed in Windows PowerShell.

## Purpose

Create a later isolated compatibility environment for the robot vendor's legacy ROS1 source after the physical robot model is identified. This environment is separate from the Ubuntu 20.04/Noetic Linker Hand environment.

Suggested Windows VM storage location:

```text
D:\cornerstone\VM\Ubuntu18_Robot_Melodic
```

No VM was created by the Windows audit.

## Entry gates

Do not start the VM build until all of the following are true:

1. The physical robot model is confirmed with nameplate photographs.
2. The arm axis count and manufacturer are confirmed.
3. The user explicitly approves creating the separate legacy VM.
4. The source-only copy set is reviewed using `FILES_TO_COPY_TO_LINUX.md`.
5. No robot, arm, chassis, or end effector is connected to the VM during the first build/audit.

## Intended baseline

- Ubuntu 18.04
- ROS Melodic
- Python compatibility determined package-by-package; do not force Python 3 across legacy scripts
- Isolated virtual network during the first source build
- No pass-through USB, CAN, serial, arm controller, or robot network connection

## Source selection

The extracted archive contains both `swiftpro` and `innfos` packages. Select packages based on the confirmed physical model:

- Julab Mini 4-axis arm: review `swiftpro` path first; L6 mechanical integration is already `BLOCKED` by payload.
- Sparrow Pro420 6-axis INNFOS arm: review `innfos` path first; do not run homing, enable, keyboard, or visual-grasp commands.

Do not infer hardware from the mere presence of both packages in the same archive.

## Offline build sequence

1. Verify `/etc/os-release` is exactly Ubuntu 18.04; otherwise stop.
2. Record OS, kernel, Python, compiler, and ROS environment.
3. Copy only reviewed source into a local virtual-disk catkin workspace; do not build under `/mnt/hgfs`.
4. Inventory `package.xml`, CMake, Python shebangs, native libraries, and architecture-specific binaries.
5. Produce a dependency plan before installing packages.
6. Build without connecting hardware and without sourcing any vendor auto-start service.
7. Run only offline unit/static tests. Do not launch `base_control`, `swiftpro`, `innfos`, navigation, web service, or visual grasp nodes.
8. Record build result as `PASS`, `FAIL`, `BLOCKED`, or `NOT_TESTED`.

## Later compatibility test design

After both isolated environments pass offline builds, plan read-only ROS1 interoperability tests for master reachability, standard topics, custom message MD5, hostname resolution, firewall, latency, and disconnect recovery. Robot-side commands remain prohibited until a separate motion-safety authorization exists.

