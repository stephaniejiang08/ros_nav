# Compatibility Matrix

Status vocabulary: `PASS`, `FAIL`, `NOT_TESTED`, `BLOCKED`, `UNKNOWN`.

| Integration question | Julab Mini + L6 | Sparrow Pro420 + L6 | Evidence / consequence |
|---|---|---|---|
| Robot model physically confirmed | UNKNOWN | UNKNOWN | Documents cannot identify the user's physical unit. |
| Robot controller baseline | PASS (documented) | PASS (documented) | Both manuals specify Ubuntu 18.04 + ROS Melodic. Actual unit remains unverified. |
| Linker ROS1 baseline | PASS (documented) | PASS (documented) | Official ROS1 SDK requires Ubuntu 20.04 + ROS Noetic + Python 3.8/3.8.10. |
| Same-OS direct deployment | BLOCKED | BLOCKED | Robot and hand vendor baselines differ; do not mix Melodic and Noetic in one untested system. |
| Arm payload capacity for bare L6 | BLOCKED | PASS only for arithmetic | Julab: 607 g > 500 g. Sparrow: 1,200 g - 607 g = 593 g before all other loads. |
| Complete mechanical payload calculation | BLOCKED | UNKNOWN | Adapter, cable, CoM, dynamics, workpiece, safety factor, and exact flange remain unresolved. |
| Existing end-effector interface reuse | UNKNOWN | BLOCKED pending redesign | Sparrow stock gripper is 0.25 kg and TTL; L6 is 0.607 kg and CAN/RS485, so mechanical/electrical/software interfaces differ. |
| L6 power design | BLOCKED | BLOCKED | Dedicated manual says max 1.4 A; later catalog says 5.6 A. Exact revision must be confirmed. |
| CAN physical interface | UNKNOWN | UNKNOWN | USB-CAN model/VID/PID/driver/interface name not supplied or connected. |
| CAN bitrate evidence | PASS (documented, not applied) | PASS (documented, not applied) | Official SDK documentation specifies 1,000,000 bit/s. No interface was configured. |
| L6 left/right configuration | UNKNOWN | UNKNOWN | Must be read from label/physical unit. |
| L6 tactile configuration | UNKNOWN | UNKNOWN | Must be confirmed from exact product option/version. |
| ROS1 message/topic interoperability | NOT_TESTED | NOT_TESTED | Requires isolated Ubuntu 20.04 and Ubuntu 18.04 environments plus MD5/topic/network tests. |
| Julab source build on Melodic | NOT_TESTED | N/A | Source contains legacy Python and bundled artifacts; no build was run on Windows. |
| Linker ROS1 SDK build on Noetic | NOT_TESTED | NOT_TESTED | Windows phase cloned only; Ubuntu phase must checkout the recorded commit and build without hardware nodes. |
| Robot network connection | BLOCKED | BLOCKED | Explicitly prohibited in the Windows phase and pending physical model confirmation. |
| Hardware motion | BLOCKED | BLOCKED | No authorization; `HARDWARE_MOTION_EXECUTED=FALSE`. |

## Recommended architecture

Use two isolated compatibility environments:

1. Ubuntu 20.04 + ROS Noetic + Python 3.8.10 for the pinned Linker ROS1 SDK and offline/mock hand integration.
2. Ubuntu 18.04 + ROS Melodic for source-only inspection/build of the verified robot model.

Only after both environments independently pass build and mock/read-only checks should a ROS1 network bridge/interoperability test be designed. A network bridge does not resolve mechanical payload or electrical safety issues.

