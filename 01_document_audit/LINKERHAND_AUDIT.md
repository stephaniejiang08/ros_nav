# Linker Hand L6 Documentation and SDK Audit

Audit time: `2026-08-03T11:04:37+08:00`

## Product facts

Primary source: `D:\cornerstone\技术文档\Linker  Hand L6 产品手册 20260402.pdf`

The dedicated L6 manual states:

- Model: Linker Hand L6
- Active control dimensions: 6 active joints plus 5 passive joints
- Mass: 607 g
- Control interfaces: CAN / RS485
- Supply: DC 24 V ±10%
- Static current: 0.2 A
- No-load average motion current: 0.75 A
- Maximum current: 1.4 A

PDF page 10 was rendered and visually inspected. The table is legible and agrees with text extraction.

## Conflicting electrical data

Secondary source: `D:\cornerstone\技术文档\灵心巧手产品手册20260707-中.pdf`

The catalog's page 12 comparison table lists L6 mass 607 g, CAN/RS485, and DC 24 V ±10%, but lists the L6 maximum current as 5.6 A and no-load average current as 0.6 A. This conflicts with the dedicated L6 manual's 1.4 A maximum and 0.75 A no-load average.

Status: `BLOCKED` for power-system sizing until Linker support confirms the correct values for the exact serial number/hardware revision. No connector pinout or supply design may be inferred from the conflicting values.

## Official SDK snapshots

The three requested repositories were cloned for static inspection only. No dependency was installed and no program was run.

| Repository | Branch | HEAD |
|---|---|---|
| `linkerhand-ros-sdk` | `main` | `2aa379cd11562d953f8b449561107b58c120676e` |
| `linkerhand-python-sdk` | `main` | `fbec1057e5320918f634fff103835d9aaa0a2269` |
| `linkerhand-ros2-sdk` | `main` | `f63bf61a03f97465844c952608e744c09bff7a2f` |

The ROS1 SDK's `doc/hardware_settings.md` explicitly requires Ubuntu 20.04, ROS Noetic, and Python 3.8, and separately calls out Python 3.8.10. The same document and README show CAN setup at bitrate `1000000` (1 Mbps). ROS1 README/configuration supports L6 over CAN and RS485.

## L6 control-vector order

The ROS1 README and the core L6 CAN implementation agree on this six-value order:

1. Thumb flexion (`thumb_cmc_pitch`)
2. Thumb lateral/yaw (`thumb_cmc_yaw`)
3. Index flexion (`index_mcp_pitch`)
4. Middle flexion (`middle_mcp_pitch`)
5. Ring flexion (`ring_mcp_pitch`)
6. Little/pinky flexion (`pinky_mcp_pitch`)

The core implementation's `get_finger_order()` returns ring before pinky. However, GUI constants in both ROS1 and Python SDKs pair the Chinese order `无名指, 小拇指` with an English list that places `pinky_mcp_pitch` before `ring_mcp_pitch`. Status: `SDK_LABEL_INCONSISTENCY`. The wire/control order above must be covered by an offline unit test before any hardware command path is enabled.

## Configuration audit

The vendor configuration defaults are examples, not verified hardware configuration:

- `hand_type`: vendor launch defaults to `right`, but physical side is `UNKNOWN`.
- `hand_joint`: defaults to `L6` and matches the target model only as a software default.
- `touch`: vendor launch defaults to `true`, but the physical tactile option/version is `UNKNOWN`.
- `can`: defaults to `can0`, but no USB-CAN was connected or identified.
- `modbus`: defaults to `None`; actual bus choice remains `UNKNOWN`.

Do not treat default values as observations.

## Safety and maintainability findings

1. `find_linker_hand.sh` actively calls `cansend` during device discovery. It is prohibited for the project's initial read-only USB-CAN inspection and must not be run.
2. Vendor README sections recommend `chmod 777` on serial devices. That is too broad for this project and must not be adopted; use exact udev/group permissions only after VID/PID identification and human approval.
3. Vendor `setting.yaml` includes a hard-coded password sample. It must not be copied into project configuration, committed, or used. Sudo credentials must be entered interactively and never stored.
4. `requirements.txt` contains many unpinned and heavy packages beyond the minimal ROS1 runtime. Installation must be planned and minimized; no bulk `pip install -r` should occur before dependency review.
5. ROS package metadata contains placeholder maintainer/license fields and no tests in `CMakeLists.txt`; successful compilation would not by itself establish functional or safety correctness.
6. Vendor examples and GUI preset actions can send motion commands. They were not executed and are excluded from the first Ubuntu phase.

## Unknown hardware facts

- Left or right hand: `UNKNOWN`
- Tactile presence/version: `UNKNOWN`
- USB-CAN model, VID/PID, driver, and interface name: `UNKNOWN`
- Exact connector/power pin assignment for the owned unit: `UNKNOWN`
- Exact hardware revision and applicable maximum-current value: `UNKNOWN`

All unknowns above block hardware startup. Static source inspection may continue, but no CAN interface activation, ROS hardware node, firmware operation, or motion command is authorized.

## Execution safety record

- SDK dependency installation: `FALSE`
- SDK program execution: `FALSE`
- CAN interface activation: `FALSE`
- CAN transmission: `FALSE`
- Hardware motion executed: `FALSE`

