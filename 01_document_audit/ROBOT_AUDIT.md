# Robot Documentation and Source Audit

Audit time: `2026-08-03T11:04:37+08:00`

## Executive result

The vendor archive contains material for two distinct robot configurations. They must not be treated as one model.

| Item | Julab Mini | Sparrow Pro420 |
|---|---|---|
| Status of documentation | PASS | PASS |
| Controller environment | Ubuntu 18.04 + ROS Melodic | Ubuntu 18.04 + ROS Melodic |
| Arm | 4-axis arm; source tree includes `swiftpro` | 6-axis INNFOS arm |
| Rated arm payload | 500 g | 1.2 kg |
| Original end effector | Suction cup or gripper options are described | 3-finger flexible gripper |
| Original gripper mass | NOT_STATED in the reviewed Julab section | 0.25 kg |
| Original gripper communication | USB/Bluetooth are listed for the arm; end-effector protocol not established | TTL serial |
| Is this the user's physical robot? | UNKNOWN | UNKNOWN |

## Julab Mini evidence

Source: `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\julab_mini-master-2\julab_mini-master\Julab mini使用说明书与快速入门手册V1.1.docx`

- Paragraph 85 states `轴数：4个`.
- Paragraph 86 states `负载：500g`.
- Paragraph 155 states the controller uses `Ubuntu18.04+ROS Melodic`.
- The manual separately identifies 24 V robot battery variants; this is not evidence that the arm's end-effector connector can directly power an L6.
- DOCX paragraphs and all seven tables were extracted structurally. Visual DOCX rendering was attempted with the required renderer, but LibreOffice/`soffice` is not installed in the available bundled runtime. Therefore DOCX visual layout QA is `NOT_TESTED`; the content facts above are based on OOXML text/table extraction.

### Static ROS source findings

The Julab source tree was read but not built or executed. Twenty package manifests were identified beneath the primary `src` tree, including:

- `base_control` 0.0.0
- `julab_mini` 1.0.0
- `swiftpro` 0.0.0
- `innfos` 0.0.0
- `visual_grab` 0.0.0
- `laser_navigation`, `ldlidar`, and `rplidar_ros`
- `human_follow`, Astra camera packages, and TurtleBot-derived packages
- `rosbridge_suite` 0.11.9 components and `web_server`

The same extracted source tree contains both `swiftpro` and `innfos`. This is a combined vendor bundle, not proof that a Julab Mini unit has an INNFOS arm. Many scripts use a generic `#!/usr/bin/env python` shebang, and at least one camera configuration explicitly uses Python 2; this is consistent with a legacy Melodic-era environment and makes a direct Noetic/Python 3 migration `NOT_TESTED`.

The archive also contains prebuilt/build artifacts, `.pyc` files, binary SDK libraries, demos, and vendor samples. These must not be copied blindly into a new workspace. A later Ubuntu 18.04 audit should start from source-only package directories, preserving the original archive separately.

## Sparrow Pro420 evidence

Source: `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\灵雀Sparrow Pro420使用说明书与快速入门手册V2.0(11-5).pdf`

- PDF page 9 states the INNFOS arm has 6 axes and a rated payload of 1.2 kg.
- PDF page 10 states the original 3-finger flexible gripper weighs 0.25 kg.
- PDF page 11 states the original gripper uses TTL serial communication.
- PDF page 17 states the controller uses Ubuntu 18.04 + ROS Melodic.
- Pages 9-11 were rendered to PNG and visually inspected; the relevant values are legible and agree with text extraction.

The manual includes procedures that enable and move the INNFOS arm. Those procedures were intentionally not run. Any commands in pages 30-34 that start `innfos_control`, publish arm commands, run keyboard control, or launch visual grasping are out of scope and remain prohibited.

## Load assessment

### Julab Mini

`607 g - 500 g = 107 g` overload before adding an adapter, cable, strain relief, or grasped object.

Result: `BLOCKED`. The L6 body alone exceeds the documented arm rating.

### Sparrow Pro420

`1200 g - 607 g = 593 g` theoretical remaining rated load.

The stock 0.25 kg gripper is 357 g lighter than the L6. Replacing it with L6 reduces the nominal residual capacity from 950 g to 593 g. That 593 g still must cover the adapter plate, fasteners, cable/strain relief, grasped object, dynamic acceleration, center-of-mass offset, and engineering safety factor.

Result: `UNKNOWN / requires physical identification and load calculation`. The arithmetic is not an integration approval.

## Physical identification gate

Before selecting any robot driver or mechanical design, a human must record:

1. Chassis and arm nameplate photographs.
2. Axis count and arm manufacturer markings.
3. Existing end-effector type and connector photographs.
4. Controller OS/ROS version from the actual unit.
5. Arm rated payload and payload convention from the exact arm datasheet.

Until then, the actual robot model remains `UNKNOWN`, robot connection remains forbidden, and no arm/chassis command may be sent.

## Execution safety record

- Robot or arm connected: `FALSE`
- ROS node launched: `FALSE`
- Demo executed: `FALSE`
- Hardware motion executed: `FALSE`

