# Files to Copy to Linux

The Windows project is the source-of-record handoff. Do not compile directly in `/mnt/hgfs`; copy the required subset to a Linux virtual disk first.

## Ubuntu 20.04 / ROS Noetic hand environment

Copy or make available read-only from the shared folder:

1. `03_linkerhand_vendor\linkerhand-ros-sdk` at commit `2aa379cd11562d953f8b449561107b58c120676e`.
2. `11_handoff\SDK_COMMITS.md`.
3. `11_handoff\WINDOWS_HANDOFF_SUMMARY.md`.
4. `01_document_audit\LINKERHAND_AUDIT.md`.
5. `01_document_audit\MISSING_INFORMATION.md`.
6. `00_source_manifest\SOURCE_MANIFEST.md`.
7. `11_handoff\UBUNTU20_CODEX_PROMPT.md`.

Optional static references only:

- `03_linkerhand_vendor\linkerhand-python-sdk` at commit `fbec1057e5320918f634fff103835d9aaa0a2269`.
- `03_linkerhand_vendor\linkerhand-ros2-sdk` at commit `f63bf61a03f97465844c952608e744c09bff7a2f`.

Do not place the ROS2 SDK inside the Noetic catkin workspace. Do not run any vendor example or discovery script during copying/audit.

Recommended Linux destination:

```text
~/cornerstone_linkerhand/vendor/linkerhand-ros-sdk
```

After copying, verify the Git HEAD and file integrity before dependency installation. The copied repository must remain at the pinned commit.

## Ubuntu 18.04 / ROS Melodic robot compatibility environment

Only after the physical robot model is confirmed, copy source-only material from:

```text
02_robot_vendor\extracted\julab_mini-master-2\julab_mini-master\src
```

Also copy the relevant robot manual and these reports:

- `01_document_audit\ROBOT_AUDIT.md`
- `01_document_audit\COMPATIBILITY_MATRIX.md`
- `01_document_audit\MISSING_INFORMATION.md`
- `11_handoff\UBUNTU18_ROBOT_VM_PLAN.md`

Exclude from the initial Melodic workspace:

- `build`, `devel`, and cached catkin outputs
- `.pyc` and `__pycache__`
- demos and scripts that command motion
- prebuilt Windows libraries
- MobaXterm installer archive
- unrelated bundled SDK samples unless later dependency analysis proves they are required

## Never copy as active configuration

- Do not copy the vendor password value from `setting.yaml` into a project configuration.
- Do not copy a vendor default `left/right`, `touch`, `can0`, or `modbus` value as though it were physically verified.
- Do not copy commands that run `cansend`, arm launch files, keyboard control, visual grasping, firmware update, or other motion paths into an automated setup script.

