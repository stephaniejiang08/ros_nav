# Missing Information and Blocking Gates

The Windows document/source audit is complete, but the following physical facts remain unresolved. Defaults in SDK examples must not be used as substitutes.

| Item | Status | Required evidence | Blocks |
|---|---|---|---|
| Actual robot model (Julab Mini vs Sparrow Pro420 or another variant) | UNKNOWN | Nameplate and whole-system photographs; axis count; controller inventory | Driver selection, payload decision, mechanical design, robot VM scope |
| L6 side | UNKNOWN | Hand label/serial-number photograph confirming left or right | SDK configuration and CAN ID selection |
| L6 tactile option/version | UNKNOWN | Purchase configuration, label, or vendor confirmation | `touch` setting, topics, data format, safety thresholds |
| USB-CAN model | UNKNOWN | Device photograph and exact model | Driver, SocketCAN support, udev rule, interface name |
| USB VID/PID and kernel driver | UNKNOWN | `lsusb`, `udevadm info`, `lsmod`, and `ip -details link` from Ubuntu with device connected | Safe udev/interface setup |
| Exact L6 hardware revision | UNKNOWN | Serial number and vendor response | Applicable current rating and protocol revision |
| L6 maximum current | BLOCKED by conflicting sources | Written confirmation for exact hardware revision; dedicated manual says 1.4 A, catalog says 5.6 A | Power supply, fuse, connector, cable sizing |
| Power/communication connector pinout | UNKNOWN | Exact revision drawing and vendor confirmation; continuity verification by qualified person | Electrical harness design |
| Adapter flange geometry and material | UNKNOWN | Arm flange drawing, L6 flange drawing, measured stack-up, fastener specification | Mechanical design and load calculation |
| Cable and strain-relief mass / routing | UNKNOWN | Selected cable assembly and routing model | Payload and collision analysis |
| Workpiece mass and center of mass | UNKNOWN | Task envelope | Payload and dynamics |
| Arm dynamic derating / safety factor | UNKNOWN | Exact arm datasheet or vendor engineering confirmation | Final payload approval |
| Robot controller IP/hostname and firewall | UNKNOWN | Read-only network plan approved by user after model confirmation | ROS network interoperability test |
| Custom ROS message MD5/topic inventory | NOT_TESTED | Both isolated ROS environments running mock/read-only nodes | Melodic-Noetic compatibility claim |

## Hard stops

- If the physical arm is the Julab Mini 500 g arm, L6 integration is `BLOCKED` because the hand alone is 607 g.
- Do not size or wire power until the 1.4 A versus 5.6 A conflict is resolved.
- Do not run `find_linker_hand.sh`; it sends CAN frames.
- Do not enable a CAN interface, run a Linker hardware node, or execute any robot/arm/hand demo without a separate explicit authorization and all required safety gates.

## Safe next evidence collection

Evidence collection may consist only of photographs, labels, purchase records, manufacturer correspondence, and later read-only Ubuntu enumeration. It must not include powering or moving the robot, arm, chassis, hand, or USB-CAN in this Windows phase.
