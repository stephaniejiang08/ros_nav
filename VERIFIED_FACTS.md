# Verified Facts

Audit snapshot: `2026-08-03T11:04:37+08:00`

This file records only facts verified from local source material or the three cloned official SDK repositories. Unknown physical configuration is not inferred from documents.

## Robot documentation

- Julab Mini manual: Ubuntu 18.04 + ROS Melodic; 4-axis arm; rated arm payload 500 g.
- Sparrow Pro420 manual: Ubuntu 18.04 + ROS Melodic; 6-axis INNFOS arm; rated payload 1.2 kg.
- Sparrow Pro420 original end effector: 3-finger flexible gripper, mass 0.25 kg, TTL serial communication.
- The extracted archive contains both `swiftpro` and `innfos` ROS packages. Their co-presence in the archive does not identify the user's physical arm.

## Linker Hand L6 documentation

- Mass: 607 g.
- Supply: DC 24 V ±10%.
- Maximum current in the dedicated L6 product manual: 1.4 A.
- Control interfaces: CAN and RS485.
- Dedicated L6 manual and the later product catalog disagree on L6 maximum current: 1.4 A versus 5.6 A. Electrical design is blocked until Linker support resolves the discrepancy for the exact hardware revision.

## Load conclusions

- Julab Mini: `607 g > 500 g`; the L6 hand alone exceeds the rated arm payload by 107 g before adapter, cable, or grasped object. Integration is `BLOCKED`.
- Sparrow Pro420: `1200 g - 607 g = 593 g` theoretical remainder before adapter plate, cable routing, safety factor, and payload. Integration requires physical identification and a full static/dynamic load calculation.

## Unknown physical facts

- Actual robot model: `UNKNOWN`.
- L6 left/right hand: `UNKNOWN`.
- Tactile option/version: `UNKNOWN`.
- USB-CAN make/model/VID/PID/driver: `UNKNOWN`.
- Exact L6 hardware revision and current limit: `UNKNOWN` because local documents conflict.

## Safety state

- Hardware connections made: `FALSE`.
- Hardware motion executed: `FALSE`.
- CAN frames transmitted: `FALSE`.
- Vendor demos or ROS nodes executed: `FALSE`.
