# VMware Workstation 17 - Ubuntu 20.04 VM Creation Guide

Status: `MANUAL_GUIDE_ONLY`. Phase 1A did not create or start a VM.

## Planned VM

| Setting | Selected value |
|---|---|
| Name | `Ubuntu20_LinkerHand_Noetic` |
| VM directory | `D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic` |
| ISO | `D:\虚拟环境\ubuntu-20.04.6-desktop-amd64.iso` |
| Guest OS | Ubuntu 20.04.6 Desktop AMD64 |
| Firmware | UEFI |
| CPU | 1 processor, 8 cores per processor (8 vCPU total) |
| Memory | 8,192 MB |
| Disk | 120 GB, growable, split into multiple files, all on D: |
| Initial network | NAT through VMnet8 |
| USB controller | USB 3.1 |
| Display | Accelerate 3D graphics; VMware-recommended graphics memory |
| Ubuntu user | `cornerstone` |
| Ubuntu hostname | `linkerhand-dev` |
| Linux workspace | `/home/cornerstone/cornerstone_linkerhand` |

The 8 GB guest memory choice reflects the host's approximately 16 GB physical RAM. The 8-vCPU choice uses one quarter of the host's 32 logical processors. D: has approximately 399 GiB free, sufficient for a 120 GiB growable virtual disk plus project data.

## Mandatory preflight - before opening the wizard

1. Confirm the ISO verification report still shows:

   ```text
   510CE77AFCB9537F198BC7DAA0E5B503B6E67AAED68146943C231BAEAAB94DF1
   OFFICIAL_HASH_VERIFIED
   ```

2. Confirm `D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic` exists and contains no unrelated files.
3. Manually repair or verify VMware NAT. Phase 1A found no registered `VMnetNat` service. Do not power on a NAT-configured VM until VMnet8 NAT is healthy.
4. Keep Linker Hand, USB-CAN, robot, arm, chassis, and robot controller physically disconnected.
5. Do not move the currently mounted ISO. If it must be moved later, first detach it and update the VM's CD/DVD path.

## VMware wizard - page-by-page

The exact wording may vary slightly within Workstation 17. Do not click **Power on this virtual machine** at the end of the wizard during Phase 1A.

### Page 1 - New Virtual Machine Wizard

Open VMware Workstation manually, then choose **File → New Virtual Machine**.

Select:

```text
Custom (advanced)
```

Reason: this exposes firmware, controller, disk, CPU, and USB choices explicitly.

Click **Next**.

### Page 2 - Hardware Compatibility

Select the installed Workstation 17.x compatibility level.

```text
Workstation 17.x
```

Click **Next**.

### Page 3 - Guest Operating System Installation

Select:

```text
I will install the operating system later.
```

This avoids VMware Easy Install and prevents any automatic installation. The verified ISO will be attached manually before the user later powers on the VM.

Click **Next**.

### Page 4 - Select a Guest Operating System

Select:

```text
Guest operating system: Linux
Version: Ubuntu 64-bit
```

Click **Next**.

### Page 5 - Name the Virtual Machine

Enter:

```text
Virtual machine name: Ubuntu20_LinkerHand_Noetic
Location: D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic
```

Verify the location begins with `D:\cornerstone\VM\`. Do not accept a default C:, Documents, or user-profile location.

Click **Next**.

### Page 6 - Firmware Type

Select:

```text
UEFI
```

Leave Secure Boot off unless the user deliberately chooses it after confirming VMware/Ubuntu compatibility. Do not change host BIOS settings.

Click **Next**.

### Page 7 - Processor Configuration

Select:

```text
Number of processors: 1
Number of cores per processor: 8
Total processor cores: 8
```

Do not select 16 or 32 vCPUs. Retain substantial host capacity for Windows and Codex.

Click **Next**.

### Page 8 - Memory for the Virtual Machine

Set:

```text
8192 MB
```

The host has approximately 15.8 GiB usable physical memory, so 12-16 GB guest allocation is not appropriate on this host.

Click **Next**.

### Page 9 - Network Type

Plan to select:

```text
Use network address translation (NAT)
```

However, do not start the VM until VMware NAT Service/VMnet8 has been manually repaired and verified. Do not select bridged networking for the initial installation. Robot networking is a later, separate phase.

Click **Next**.

### Page 10 - I/O Controller Type

Use VMware's recommended controller for Ubuntu 64-bit. For Workstation 17 this is normally the recommended LSI Logic or default choice presented by the wizard.

Do not override the recommended controller without a documented compatibility reason.

Click **Next**.

### Page 11 - Virtual Disk Type

Use VMware's recommended modern disk type for this guest, normally NVMe when offered and supported by the selected hardware compatibility.

If NVMe is not offered, retain VMware's recommended SCSI type. Do not attach a physical disk.

Click **Next**.

### Page 12 - Select a Disk

Select:

```text
Create a new virtual disk
```

Do not use a physical disk and do not reuse an unrelated VMDK.

Click **Next**.

### Page 13 - Specify Disk Capacity

Set:

```text
Maximum disk size: 120 GB
Allocate all disk space now: unchecked
Split virtual disk into multiple files: selected
```

The disk must grow on demand and remain entirely under the D: VM directory.

Click **Next**.

### Page 14 - Specify Disk File

Keep the disk file under:

```text
D:\cornerstone\VM\Ubuntu20_LinkerHand_Noetic
```

A clear name such as `Ubuntu20_LinkerHand_Noetic.vmdk` is recommended.

Click **Next**.

### Page 15 - Ready to Create Virtual Machine

Before finishing, choose **Customize Hardware**.

Do not power on yet.

## Customize Hardware

### CD/DVD

Select **Use ISO image file** and browse to:

```text
D:\虚拟环境\ubuntu-20.04.6-desktop-amd64.iso
```

Enable **Connect at power on** only when the user is ready to perform the manual Ubuntu installation.

### USB Controller

Select:

```text
USB compatibility: USB 3.1
```

Do not connect or auto-connect USB-CAN, Linker Hand, robot, or serial devices. USB pass-through is reserved for a later read-only identification phase.

### Display

Enable:

```text
Accelerate 3D graphics
```

Use VMware's recommended graphics-memory setting. Do not allocate excessive host graphics memory.

### Network Adapter

Keep NAT selected, but treat VM power-on as blocked until VMnet8 NAT is healthy.

### Shared Folders

Leave shared folders disabled for the initial OS installation. After Ubuntu is installed and VMware Tools/open-vm-tools is ready, share only:

```text
D:\cornerstone\shared
```

Do not share C:, the user profile, Documents, Desktop, Downloads, OneDrive, or the entire D: drive.

### Unneeded devices

Remove or disable unneeded printer, Bluetooth, camera, sound, and other pass-through devices unless the user has a later documented requirement.

Click **Close**, then **Finish**.

## Stop after VM definition

At the end of Phase 1A:

- Do not start the VM.
- Do not boot the ISO.
- Do not install Ubuntu.
- Do not install ROS.
- Do not attach USB devices.

## Later manual Ubuntu installation choices

When the user later explicitly starts the installation:

- Ubuntu user: `cornerstone`
- Computer name/hostname: `linkerhand-dev`
- Use the entire 120 GB virtual disk only; never select a host physical disk.
- Do not enable third-party drivers or online accounts unless separately reviewed.
- After installation, create `/home/cornerstone/cornerstone_linkerhand` on the guest ext4 filesystem.
- Copy sources from `/mnt/hgfs/windows_to_ubuntu/linkerhand_handoff` into Linux home before building.
- Never run `catkin_make`, `catkin build`, or `colcon` under `/mnt/hgfs`.

## Recommended checkpoints after later installation

Create manual snapshots only after the user authorizes and completes each stage:

1. `ubuntu20_clean_install`
2. `noetic_installed_verified`
3. `linkerhand_sdk_pinned_build`
4. `mock_tests_passed_no_hardware`

No snapshot or VM was created in Phase 1A.
