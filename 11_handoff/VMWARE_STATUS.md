# VMware and Host Virtualization Status

Checked on: `2026-08-03` (Asia/Shanghai)

No installer, repair action, Windows feature change, BIOS change, reboot, or VM launch was performed.

## VMware Workstation

| Item | Observed value | Status |
|---|---|---|
| Product | VMware Workstation | INSTALLED |
| Registry display version | `17.0.0` | PASS |
| Product version/build | `17.0.0.20800274` / build `20800274` | PASS |
| Main executable | `D:\Program Files\vmware.exe` | PASS |
| Main executable version | `17.0.0 build-20800274` | PASS |
| Registered install path | `D:\Program Files\` | PASS |
| VMware Player executable | `D:\Program Files\vmplayer.exe` | PRESENT |

## VMware services

| Service | State | Start type | Finding |
|---|---|---|---|
| VMware DHCP Service (`VMnetDHCP`) | Running | Automatic | PASS |
| VMware USB Arbitration Service (`VMUSBArbService`) | Running | Automatic | PASS |
| VMware Authorization Service (`VMAuthdService`) | Running | Automatic | PASS |
| VMware NAT Service (`VMnetNat`) | Not found | N/A | BLOCKED for planned NAT networking |
| VMware Host Agent (`VMwareHostd`) | Not found | N/A | INFORMATIONAL; not used as proof of workstation failure |

Additional static observations:

- `D:\Program Files\vmnat.exe` exists and reports version `17.0.0 build-20800274`.
- VMware registry configuration contains `vmnet1` and `vmnet8`, including a `vmnet8\NAT` configuration key.
- The NAT service itself is not registered/readable through Windows Service Control Manager.

Conclusion: VMware is installed, but NAT is not ready for the planned first-stage network. Before powering on the VM, a human must open VMware Virtual Network Editor and verify/repair VMnet8 NAT or run an approved VMware repair workflow. No automatic repair was performed.

## CPU and firmware virtualization

| Item | Value | Status |
|---|---|---|
| CPU | AMD Ryzen 9 8945HX with Radeon Graphics | PASS |
| Physical cores | 16 | PASS |
| Logical processors | 32 | PASS |
| Firmware virtualization enabled | `True` | PASS |
| Hypervisor present | `True` | INFORMATIONAL |
| VM monitor mode extensions reported to guest OS query | `False` | UNKNOWN under active hypervisor |
| Second-level address translation reported to guest OS query | `False` | UNKNOWN under active hypervisor |

`systeminfo` reported that a hypervisor is already detected, so Windows did not display its normal Hyper-V requirement details. Firmware virtualization is explicitly reported as enabled. A later manual VMware launch test is still required because this phase forbids starting a VM.

## Windows hypervisor and optional features

Direct `Get-WindowsOptionalFeature -Online` queries required an administrator token that was not available. No UAC elevation or feature change was attempted.

Read-only evidence:

- Windows reports `HypervisorPresent=True`.
- Device Guard registry: virtualization-based security enabled.
- Hypervisor-enforced code integrity registry: enabled.
- `HvHost` service is running.
- `vmcompute` service exists and is stopped/manual.
- Hyper-V Virtual Machine Management service (`vmms`) is not present.
- `WslService` exists but is disabled/stopped.
- `wsl.exe --status` and distribution listing failed with `0x80070422`; no WSL distribution state was obtained.

Because package-registry presence is not the same as optional-feature enablement, exact feature states are conservatively recorded as follows:

| Windows feature | Status |
|---|---|
| Hyper-V full feature | UNKNOWN; active Windows hypervisor/VBS observed, `vmms` absent |
| Virtual Machine Platform | UNKNOWN; `vmcompute` present |
| Windows Hypervisor Platform | UNKNOWN; active hypervisor observed |
| Windows Sandbox | UNKNOWN |
| WSL optional feature | UNKNOWN; CLI present, service disabled, status query failed |

Do not automatically disable any Windows security or virtualization feature. If VMware later reports a compatibility error, record the exact message first and let the user choose the remediation.

## Host resources

| Resource | Value | Phase 1A decision |
|---|---:|---|
| Physical memory | `16,962,326,528` bytes (`15.797` GiB) | Allocate 8 GiB to VM |
| Logical processors | 32 | Allocate 8 vCPU (1 socket × 8 cores) |
| D: total | `551.645` GiB | PASS |
| D: free | `399.374` GiB | PASS for 120 GiB growable VM plus project data |

## Readiness result

- VMware installed: `PASS`
- CPU firmware virtualization: `PASS`
- Memory sizing: `PASS` with 8 GiB guest allocation
- D: capacity for 120 GiB growable disk: `PASS`
- NAT readiness: `BLOCKED` until `VMnetNat`/VMnet8 is manually repaired or verified
- USB arbitration service: `PASS`, but no USB-CAN may be connected in this phase
- VM creation/start: `NOT_EXECUTED`
