# Next Actions

## Immediate human evidence collection

1. Photograph the robot chassis and arm nameplates, the full arm, existing gripper, flange, connectors, and Linker Hand label/serial number.
2. Confirm whether the hand is left or right and whether it includes tactile sensing; obtain the exact tactile version.
3. Identify the USB-CAN make/model before connecting it to any VM.
4. Ask Linker support to resolve the 1.4 A versus 5.6 A L6 maximum-current conflict for the exact serial number and provide the exact connector/pinout drawing.
5. If the robot is Sparrow Pro420, obtain adapter/cable mass and workpiece envelope and perform a static/dynamic payload and center-of-mass calculation.
6. If the robot is Julab Mini with the documented 500 g arm, stop L6 arm integration; the hand alone is over payload.

## Next software phase

Use `11_handoff\UBUNTU20_CODEX_PROMPT.md` only inside an Ubuntu 20.04 VM. The prompt must first validate `/etc/os-release` and must stop on any other version.

The first Ubuntu phase is limited to:

- official ROS Noetic installation after environment validation;
- copying and checking out ROS1 SDK commit `2aa379cd11562d953f8b449561107b58c120676e`;
- dependency planning and offline build;
- mock, dry-run, safety lock, and unit tests;
- read-only USB enumeration only if separately approved later.

Do not run `find_linker_hand.sh`, vendor GUIs/presets, any robot package, firmware tools, `cansend`, or hardware nodes.

## Safety state

`HARDWARE_MOTION_EXECUTED=FALSE`
