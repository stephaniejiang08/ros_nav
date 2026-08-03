# Ubuntu 20.04 Codex Prompt - Linker Hand L6 Safe Phase

You are running inside an Ubuntu virtual machine. Execute this prompt only for the Linker Hand L6 integration preparation described below.

## Absolute safety scope

- This phase may install ROS Noetic, copy and build the pinned ROS1 SDK, and create offline mock/safety tests.
- Do not connect to or control a robot, mechanical arm, chassis, Linker Hand, USB-CAN, serial converter, or robot network.
- Do not run any command that can move hardware.
- Do not run vendor demos, GUI preset actions, ROS hardware nodes, firmware tools, `cansend`, or `find_linker_hand.sh`.
- Do not install ROS2, WSL, Docker, or a second ROS distribution.
- Do not build in `/mnt/hgfs`.
- Sudo passwords must be typed interactively and must never be stored in a file, command history helper, YAML file, or report.
- Do not adopt vendor recommendations to use `chmod 777`.
- `HARDWARE_MOTION_EXECUTED` must remain `FALSE`.

## Step 0 - mandatory OS gate before any modification

The first command must be:

```bash
cat /etc/os-release
```

Parse the file and require both:

```text
ID=ubuntu
VERSION_ID="20.04"
```

If either value differs, immediately print:

```text
UBUNTU_20_04_REQUIRED
HARDWARE_MOTION_EXECUTED=FALSE
```

Then stop. Do not install, update, copy, or configure anything.

## Step 1 - locate and verify the Windows handoff

Expected shared path:

```text
/mnt/hgfs/cornerstone/codex/linkerhand_composite_robot
```

Require these files:

```text
11_handoff/WINDOWS_HANDOFF_SUMMARY.md
11_handoff/SDK_COMMITS.md
11_handoff/FILES_TO_COPY_TO_LINUX.md
01_document_audit/LINKERHAND_AUDIT.md
01_document_audit/MISSING_INFORMATION.md
03_linkerhand_vendor/linkerhand-ros-sdk/.git
```

If the handoff path or any required file is absent, print:

```text
WINDOWS_HANDOFF_NOT_FOUND
HARDWARE_MOTION_EXECUTED=FALSE
```

Then stop. Do not clone a replacement and do not guess missing configuration.

Read the handoff reports. Confirm the Windows-recorded ROS1 commit is exactly:

```text
2aa379cd11562d953f8b449561107b58c120676e
```

## Step 2 - read-only environment audit

Run and record:

```bash
cat /etc/os-release
uname -a
hostname
whoami
python3 --version
pip3 --version
df -h
free -h
groups
env | grep '^ROS' || true
```

Do not enumerate or configure USB/CAN in this phase unless the user gives a separate later approval. Do not connect any hardware for the audit.

Create only on the VM's Linux virtual disk:

```text
~/cornerstone_linkerhand/logs
~/cornerstone_linkerhand/reports
~/cornerstone_linkerhand/config
~/cornerstone_linkerhand/vendor
~/cornerstone_linkerhand/linkerhand_noetic_ws/src
~/cornerstone_linkerhand/integration_ws/src
```

Write the raw audit to `logs/environment_raw.txt` and the summarized audit to `reports/UBUNTU_ENVIRONMENT.md`.

## Step 3 - system-change approval gate

Before any apt/source/key modification, print the exact commands you intend to run. Use only current official ROS Ubuntu 20.04/Noetic instructions and official repositories/keys. Do not use third-party one-line installers.

Wait for the user to approve the displayed commands. When sudo is required, let the user type the password interactively. Do not record it.

Install only the required baseline:

- `ros-noetic-desktop-full`
- rosdep tooling
- `catkin-tools`
- `git`
- `build-essential`
- `can-utils` for later read-only diagnostics only

Do not upgrade Ubuntu to another release and do not install ROS2.

Before editing `~/.bashrc`, create `~/.bashrc.backup_before_linkerhand`. Preserve any existing ROS configuration and add `source /opt/ros/noetic/setup.bash` only once.

Initialize/update rosdep using the standard official procedure. Record every command and result without capturing credentials.

## Step 4 - ROS installation verification

Verify:

```bash
source /opt/ros/noetic/setup.bash
rosversion -d
```

Run `roscore` only long enough to verify `rosnode list` and `rostopic list`, then shut it down cleanly. No vendor node may be started.

If ROS installation or verification fails, record `FAIL`, print `ROS_NOETIC_INSTALL_FAILED`, and stop.

## Step 5 - copy and pin the ROS1 SDK

Copy the Windows-audited repository from the shared folder into the VM local filesystem. Do not compile under `/mnt/hgfs`.

Recommended destination:

```text
~/cornerstone_linkerhand/vendor/linkerhand-ros-sdk
```

After copying, verify:

```bash
git -C ~/cornerstone_linkerhand/vendor/linkerhand-ros-sdk remote get-url origin
git -C ~/cornerstone_linkerhand/vendor/linkerhand-ros-sdk rev-parse HEAD
git -C ~/cornerstone_linkerhand/vendor/linkerhand-ros-sdk status --short
```

Checkout the exact audited commit in detached mode if needed:

```text
2aa379cd11562d953f8b449561107b58c120676e
```

If the commit is unavailable or the source differs from the Windows handoff, print `SDK_COMMIT_MISMATCH` and stop. Do not update to latest `main`.

Copy the ROS1 repository into `~/cornerstone_linkerhand/linkerhand_noetic_ws/src` in a way that preserves the audited source. Do not modify vendor files in place.

## Step 6 - dependency plan before installation

Statically inspect:

- `README.md` and `README_CN.md`
- `requirements.txt`
- `package.xml`
- `CMakeLists.txt`
- launch files
- `LinkerHand/config/setting.yaml`
- L6 CAN and RS485 implementations
- examples, without running them

Create `reports/DEPENDENCY_PLAN.md` before installing SDK dependencies.

The vendor `requirements.txt` contains many unpinned/heavy packages. Do not blindly run `pip install -r requirements.txt`. Identify the minimal packages required to import/build the core ROS1 L6 SDK. Prefer apt for ROS/system dependencies and `python3 -m pip install --user` only for reviewed Python packages. Never use `sudo pip`, `--break-system-packages`, or arbitrary core-package upgrades.

Use rosdep to review workspace dependencies. Do not run hardware discovery as a dependency check.

## Step 7 - build only

Use one build method consistently; default to `catkin_make` unless the audited package explicitly requires another method.

Write the full build log to:

```text
~/cornerstone_linkerhand/logs/linkerhand_build.log
```

Do not source or launch the vendor hardware node after building. Do not run examples or GUI actions.

If the build fails, create `reports/BUILD_RESULT.md` with `FAIL`, print `LINKERHAND_BUILD_FAILED`, and stop.

## Step 8 - safe project configuration

Do not copy the vendor password value or vendor hardware defaults as verified facts.

Create `config/hardware_lock.yaml` containing:

```yaml
hardware_enabled: false
allow_motion: false
allow_firmware_update: false
allow_robot_connection: false
dry_run: true
max_command_rate_hz: 5
command_timeout_sec: 1.0
```

Create `config/linkerhand_l6.yaml` with unknown physical values explicitly blocked:

```yaml
hand_type: UNKNOWN
hand_joint: L6
touch: UNKNOWN
can: UNKNOWN
modbus: UNKNOWN
hardware_revision: UNKNOWN
```

All custom code must load `hardware_lock.yaml`, fail closed when a field is missing, and prohibit hardware startup while any physical item is `UNKNOWN`.

The audited six-value L6 order is:

```text
thumb flexion, thumb yaw/lateral, index, middle, ring, pinky
```

Add an offline unit test that catches the vendor GUI English-label inconsistency where ring and pinky are reversed. Do not test the mapping on hardware.

## Step 9 - offline mock and tests

Create mock/safety packages and tests only. They must cover:

- fake joint states and tactile data
- command bounds and timeout
- CAN-disconnected state
- grasp success/failure simulation
- dry-run and hardware-enabled lock
- emergency stop
- maximum retry count with no infinite retry
- all motion paths blocked by default

Use standard ROS messages where practical. Do not start the official Linker hardware node during tests.

## Step 10 - reports and stop

Create:

```text
reports/PHASE1_SUMMARY.md
reports/BUILD_RESULT.md
reports/COMPATIBILITY_RESULT.md
reports/NEXT_HARDWARE_STEPS.md
```

Use only `PASS`, `FAIL`, `NOT_TESTED`, `BLOCKED`, and `UNKNOWN` status labels.

The summary must state:

- the exact pinned commit;
- ROS/build/mock results;
- physical robot model remains `UNKNOWN`;
- left/right, tactile option, and USB-CAN remain `UNKNOWN`;
- Julab Mini L6 load result is `BLOCKED`;
- Sparrow Pro420 result requires physical identification and load calculation;
- the 1.4 A versus 5.6 A L6 current conflict is unresolved;
- no hardware motion was executed.

If all Windows handoff verification, Ubuntu 20.04 environment, ROS Noetic verification, pinned SDK build, and offline tests complete successfully, print:

```text
PHASE1_UBUNTU_NOETIC_COMPLETE
REPORT=~/cornerstone_linkerhand/reports/PHASE1_SUMMARY.md
BUILD_REPORT=~/cornerstone_linkerhand/reports/BUILD_RESULT.md
HARDWARE_MOTION_EXECUTED=FALSE
```

Then stop. Do not enter hardware setup, CAN activation, robot networking, or motion testing.
