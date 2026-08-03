# Windows Handoff Summary

Status: `WINDOWS_HANDOFF_READY`

Project root: `D:\cornerstone\codex\linkerhand_composite_robot`

Audit time: `2026-08-03T11:04:37+08:00`

## Scope completed

- Located and hashed local robot and Linker Hand documentation.
- Extracted the composite robot archive and its embedded Julab Mini archive without executing any contents.
- Kept Julab Mini and Sparrow Pro420 as distinct robot configurations.
- Performed static document and ROS source audit.
- Cloned and pinned the official ROS1, Python, and ROS2 Linker Hand SDKs.
- Prepared separate Ubuntu 20.04/Noetic hand and Ubuntu 18.04/Melodic robot plans.
- Did not install Ubuntu, ROS, WSL, Docker, a VM, or SDK dependencies.
- Did not connect or operate any hardware.

## Actual source paths

- L6 dedicated manual: `D:\cornerstone\技术文档\Linker  Hand L6 产品手册 20260402.pdf`
- Linker product catalog: `D:\cornerstone\技术文档\灵心巧手产品手册20260707-中.pdf`
- Composite robot ZIP: `D:\cornerstone\技术文档\哈工大（合肥）创新研究院复合机器人.zip`
- Julab Mini manual/source: `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\julab_mini-master-2\julab_mini-master`
- Sparrow Pro420 manual: `D:\cornerstone\codex\linkerhand_composite_robot\02_robot_vendor\extracted\灵雀Sparrow Pro420使用说明书与快速入门手册V2.0(11-5).pdf`
- Official SDK clones: `D:\cornerstone\codex\linkerhand_composite_robot\03_linkerhand_vendor`

See `00_source_manifest\SOURCE_MANIFEST.md` for SHA256 values.

## Robot identity and load risk

The actual physical robot model remains `UNKNOWN`; documents alone cannot determine whether the unit is Julab Mini, Sparrow Pro420, or another configuration.

### If the arm is Julab Mini

- Documented arm: 4 axes, rated payload 500 g.
- L6 mass: 607 g.
- Result: `BLOCKED`. The L6 body alone is 107 g over the arm rating, before adapter, cable, or object.

### If the arm is Sparrow Pro420

- Documented arm: 6-axis INNFOS, rated payload 1.2 kg.
- Original gripper: 0.25 kg, TTL serial.
- Arithmetic: `1200 g - 607 g = 593 g` theoretical remainder.
- Result: `需实物确认与负载核算`. The 593 g must still cover adapter, fasteners, cable/strain relief, object, center-of-mass offset, dynamic loads, and safety factor.

## L6 verified facts and blockers

- Verified from the dedicated L6 manual: 607 g, DC 24 V ±10%, CAN/RS485, maximum current 1.4 A.
- The later product catalog lists 5.6 A maximum current for L6, conflicting with the dedicated manual. Power-system design is `BLOCKED` until the exact hardware revision is confirmed by Linker support.
- Left/right hand: `UNKNOWN`.
- Tactile option/version: `UNKNOWN`.
- USB-CAN model/VID/PID/driver: `UNKNOWN`.

## Pinned SDK commits

- ROS1: `2aa379cd11562d953f8b449561107b58c120676e`
- Python: `fbec1057e5320918f634fff103835d9aaa0a2269`
- ROS2: `f63bf61a03f97465844c952608e744c09bff7a2f`

See `11_handoff\SDK_COMMITS.md` for URLs, branches, timestamps, subjects, and the exact checkout rule.

## SDK safety findings

- Official ROS1 documentation requires Ubuntu 20.04 + ROS Noetic + Python 3.8/3.8.10 and specifies 1 Mbps CAN.
- `find_linker_hand.sh` calls `cansend`; do not run it in a read-only hardware inspection.
- Vendor `setting.yaml` includes a stored password sample and vendor docs suggest overly broad device permissions. Do not copy either practice.
- L6 core order is thumb flexion, thumb yaw, index, middle, ring, pinky. GUI English labels reverse the final two names relative to the Chinese labels/core order; add offline unit tests before any hardware command path.

## Environment recommendation

1. First build an isolated Ubuntu 20.04 + ROS Noetic + Python 3.8.10 hand-development VM using the pinned ROS1 SDK. Initial work must be compile, mock, dry-run, and read-only only.
2. Later build a separate Ubuntu 18.04 + ROS Melodic robot-compatibility VM, but only after the physical robot model is identified.
3. Do not install Melodic and Noetic into one environment and do not claim cross-version compatibility until network, topic, standard-message, custom-message MD5, latency, and disconnect behavior are tested.

## Documentation QA note

- Relevant PDF pages were rendered and visually inspected.
- The Julab DOCX was structurally inspected (paragraphs and tables). Visual DOCX rendering was attempted, but LibreOffice/`soffice` was unavailable; DOCX layout QA is `NOT_TESTED`. This limitation does not affect the extracted 4-axis, 500 g, and Ubuntu 18.04/Melodic text facts.

## Safety declaration

- Robot connected: `FALSE`
- Mechanical arm connected: `FALSE`
- Chassis connected: `FALSE`
- Linker Hand connected: `FALSE`
- USB-CAN connected: `FALSE`
- CAN frames sent: `FALSE`
- Vendor demo/ROS node executed: `FALSE`
- `HARDWARE_MOTION_EXECUTED=FALSE`

