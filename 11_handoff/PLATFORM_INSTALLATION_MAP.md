# Platform Installation Map

Ubuntu is the Linux distribution used by this project. There is no separate operating system named “Linux” that must be downloaded in addition to Ubuntu.

## Windows host

Install/store here:

- VMware Workstation Pro
- Project documentation and local Git repository
- Ubuntu ISO and VM files on D:
- Windows-to-Ubuntu and Ubuntu-to-Windows shared handoff folders

Do not install here:

- ROS Noetic
- ROS Melodic
- Linux CAN drivers intended for the guest
- Linker Hand hardware runtime

Current project root:

```text
D:\cornerstone\codex\linkerhand_composite_robot
```

## Ubuntu 20.04 virtual machine

Purpose:

- ROS Noetic
- Python 3.8 / audited Python 3.8.10 baseline
- Pinned Linker Hand ROS1 SDK
- Linker Hand mock nodes and isolated offline tests
- Safety lock and dry-run code
- Later read-only USB/USB-CAN identification, after a separate approval

VM name and location:

```text
Ubuntu20_LinkerHand_Noetic
D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic
```

Linux workspace:

```text
/home/cornerstone/cornerstone_linkerhand
```

Do not build catkin workspaces directly in `/mnt/hgfs`. Copy the handoff source into the VM's ext4 virtual disk and build there. Because the VMDK is stored on D:, Linux home data still physically resides on D:.

## Ubuntu 18.04 virtual machine - later and optional

Purpose only after the physical robot model is confirmed:

- ROS Melodic
- The verified robot model's original vendor ROS packages
- Offline compatibility reproduction

Do not create this VM during Phase 1A. Do not copy the combined robot vendor source into the Ubuntu 20.04 hand workspace.

## Robot controller

The documentation suggests that Julab Mini and Sparrow Pro420 controllers use Ubuntu 18.04 + ROS Melodic. This is a documentation fact, not proof of the actual physical robot.

The real controller OS, ROS distribution, robot model, arm model, network configuration, and software version must be read from the physical system later. Do not deploy vendor programs or connect to the robot ROS Master until those facts are confirmed and separately authorized.

## Separation rule

| Platform | ROS | Primary responsibility |
|---|---|---|
| Windows | None | VMware, project files, Git, handoff storage |
| Ubuntu 20.04 VM | Noetic | Linker Hand ROS1 SDK, mock, safety, offline tests |
| Ubuntu 18.04 VM (optional) | Melodic | Confirmed robot vendor source compatibility |
| Physical robot controller | UNKNOWN until inspected | Existing robot runtime only; no Phase 1A connection |
