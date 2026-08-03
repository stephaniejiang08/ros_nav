# Phase 1A Windows Preparation Summary

Status: `PHASE1A_WINDOWS_PREPARATION_COMPLETE`

Project root: `D:\cornerstone\codex\linkerhand_composite_robot`

Scope: Windows-side Ubuntu 20.04 VMware planning, source audit, and Linux handoff generation only. No VMware/Ubuntu/ROS/driver installation, VM startup, hardware connection, CAN transmission, SDK execution, firmware action, or motion was performed.

## Ubuntu ISO verification

- Actual ISO path: `D:\虚拟环境\ubuntu-20.04.6-desktop-amd64.iso`
- Exact size: 4,351,463,424 bytes (4.052616 GiB)
- Local SHA256: `510ce77afcb9537f198bc7daa0e5b503b6e67aaed68146943c231baeaaab94df1`
- Full-file read/hash: `PASS`
- Ubuntu official SHA256 match: `PASS`
- Official checksum source: `https://releases.ubuntu.com/20.04/SHA256SUMS`
- Mounted media relation: disk image attached read-only as `\\.\CDROM0`, drive `E:`, CDFS label `Ubuntu 20.04.6 L`
- ISO moved, extracted, or executed: `FALSE`

## VMware and host status

- VMware Workstation installation found: `17.0.0 build-20800274`
- Main program: `D:\Program Files\vmware.exe`
- DHCP service: running/automatic
- USB Arbitration service: running/automatic
- Authorization service: running/automatic
- VMware NAT executable and vmnet8 NAT registry configuration: present
- `VMnetNat` service: not found; NAT readiness is `BLOCKED` until the user manually verifies/repairs it in VMware Virtual Network Editor or an approved VMware Repair workflow
- Host CPU: AMD Ryzen 9 8945HX, 16 physical / 32 logical cores
- Firmware virtualization flag: enabled
- Host memory: 16,962,326,528 bytes (15.797 GiB); VM recommendation reduced to 8 GiB
- D: free space at audit: 399.374 GiB; sufficient for a 120 GB growable virtual disk
- Hypervisor/VBS: an active Windows hypervisor and VBS/HVCI were observed
- Exact optional-feature states: `UNKNOWN` because the read-only query requires an elevated administrator session; no feature was modified

## VM plan

- Name: `Ubuntu20_LinkerHand_Noetic`
- Planned directory: `D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic`
- Firmware: UEFI
- CPU: one processor, eight virtual cores
- Memory: 8,192 MB
- Disk: 120 GB, growable, split into multiple files, all on D:
- Network: NAT only after the NAT blocker is manually resolved
- USB: USB 3.1, with no device attached during Phase 1A
- Shared folder: initially disabled; later restrict to `D:\cornerstone\shared`
- VM created or powered on: `FALSE`
- Guide: `11_handoff\UBUNTU20_VM_CREATION_GUIDE.md`

## Fixed SDK verification

All three source repositories were found under the actual path `D:\cornerstone\codex\linkerhand_composite_robot\03_linkerhand_vendor`, matched their Phase 0 pins, and had clean worktrees:

- ROS1: `2aa379cd11562d953f8b449561107b58c120676e`
- Python: `fbec1057e5320918f634fff103835d9aaa0a2269`
- ROS2: `f63bf61a03f97465844c952608e744c09bff7a2f`

No repository was fetched, pulled, switched, updated, or executed. The Linux handoff includes only an exact `git archive` snapshot of the pinned ROS1 commit: 309 files, 10,628,786 bytes, no `.git` metadata and no forbidden ISO/EXE/archive/video/model-package extension.

## Linux handoff

- Root: `D:\cornerstone\shared\windows_to_ubuntu\linkerhand_handoff`
- Ubuntu prompt: `PHASE1_UBUNTU_CODEX_PROMPT.md`
- Safety defaults: `config\hardware_lock.yaml`
- Print-only installation draft: `scripts\phase1_install_plan_draft.sh`
- Read-only USB-CAN guide: `guides\USB_CAN_READONLY_GUIDE.md`
- SDK risk register: `SDK_RISK_REGISTER.md`
- Prohibited execution paths: `PROHIBITED_SCRIPTS.md`
- Pinned source: `sdk\linkerhand-ros-sdk`
- Integrity controls: `HANDOFF_MANIFEST.md` and `HANDOFF_SHA256SUMS.txt`

The package deliberately excludes the Ubuntu ISO, VMware installer, Windows executables, videos, large external models, robot archives, robot vendor programs, ROS2 SDK, Python SDK, and unrelated robot software.

## Remaining blockers

- VMware NAT service must be manually verified/repaired before any VM is started.
- Actual robot model, L6 side, tactile option/version, USB-CAN model/VID:PID/driver/interface, exact L6 hardware revision, connector pinout, arm load limits, and robot controller identity remain unknown.
- The L6 maximum-current conflict (1.4 A versus 5.6 A) blocks power/harness design.
- If the physical arm is the Julab Mini rated at 500 g, the 607 g L6 hand alone exceeds the payload and integration is blocked.

## Execution record

- `VMWARE_INSTALL_EXECUTED=FALSE`
- `UBUNTU_INSTALL_EXECUTED=FALSE`
- `ROS_INSTALL_EXECUTED=FALSE`
- `SDK_PROGRAM_EXECUTED=FALSE`
- `CAN_TRANSMISSION_EXECUTED=FALSE`
- `HARDWARE_CONNECTION_EXECUTED=FALSE`
- `HARDWARE_MOTION_EXECUTED=FALSE`
