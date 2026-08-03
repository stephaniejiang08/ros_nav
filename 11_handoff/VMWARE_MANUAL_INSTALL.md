# VMware Manual Installation / Repair Checklist

## Current decision

VMware Workstation is already installed:

```text
Version: 17.0.0 build-20800274
Main executable: D:\Program Files\vmware.exe
```

Therefore a fresh VMware installation is not required and was not performed.

## Manual preflight before VM creation

1. Do not run VMware or any installer as part of the automated Windows audit.
2. When the user is ready, open VMware Workstation manually.
3. Open **Edit → Virtual Network Editor** using an administrator-approved UI action.
4. Check that `VMnet8` exists, is set to NAT, has DHCP enabled, and has a valid subnet.
5. Check Windows Services for **VMware NAT Service**. It is currently not found even though `vmnat.exe` and vmnet8 NAT registry configuration exist.
6. If NAT remains missing, close VMware and perform a manual VMware **Repair** using a trusted VMware Workstation 17 installer matching the installed product.
7. During repair, do not relocate the project, ISO, or VM folders to C:.
8. After repair, verify `VMnetNat`, `VMnetDHCP`, `VMUSBArbService`, and `VMAuthdService` before creating or starting the VM.

## Hypervisor caution

Windows currently reports an active hypervisor and enabled virtualization-based security. Do not automatically disable Hyper-V-related components, Device Guard, memory integrity, or BIOS virtualization.

If VMware displays a compatibility or performance error:

1. Capture the exact VMware error text and version.
2. Record the current Windows optional-feature states from an administrator PowerShell session.
3. Evaluate VMware's supported coexistence mode first.
4. Obtain explicit user approval before disabling any Windows feature.
5. Reboot only when the user explicitly chooses and performs the change.

## Prohibited automated actions

- No VMware installer execution
- No silent install or repair
- No `Disable-WindowsOptionalFeature`
- No `bcdedit` modification
- No registry modification
- No BIOS change
- No automatic reboot
- No VM creation or launch

`VMWARE_INSTALL_EXECUTED=FALSE`
