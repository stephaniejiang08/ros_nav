# Ubuntu 20.04.6 ISO Verification

Checked on: `2026-08-03` (Asia/Shanghai)

## Local file

| Field | Value | Status |
|---|---|---|
| Path | `D:\虚拟环境\ubuntu-20.04.6-desktop-amd64.iso` | PASS |
| Exact size | `4,351,463,424` bytes | PASS |
| Size in GiB | `4.052616` GiB | INFORMATIONAL |
| SHA256 | `510CE77AFCB9537F198BC7DAA0E5B503B6E67AAED68146943C231BAEAAB94DF1` | PASS |
| File read test | First 4,096 bytes read successfully; SHA256 required reading the complete file | PASS |
| File modified | No | PASS |
| ISO extracted | No | PASS |
| Program executed from ISO | No | PASS |

## Official hash verification

Official Ubuntu SHA256 source:

```text
https://releases.ubuntu.com/20.04/SHA256SUMS
```

The official entry is:

```text
510ce77afcb9537f198bc7daa0e5b503b6e67aaed68146943c231baeaab94df1 *ubuntu-20.04.6-desktop-amd64.iso
```

The locally calculated SHA256 matches the official Ubuntu value exactly.

Result: `OFFICIAL_HASH_VERIFIED`.

This conclusion is based on a full SHA256 comparison, not merely on the ability to mount the file.

## Windows mount association

Windows storage inspection reported:

| Field | Value |
|---|---|
| Disk image path | `D:\虚拟环境\ubuntu-20.04.6-desktop-amd64.iso` |
| Attached | `True` |
| Device path | `\\.\CDROM0` |
| Associated drive | `E:` |
| Volume label | `Ubuntu 20.04.6 L` |
| Filesystem | `CDFS` |
| Drive type | `CD-ROM` |
| Volume health | `Healthy` |
| Mounted size | `4,351,463,424` bytes |
| Size remaining | `0` bytes (read-only optical filesystem) |

Result: `E:` is the Windows read-only mount of the specified ISO.

No file was opened or executed from `E:` and no write was attempted.

## Storage policy

The ISO remains at its original path. It was not moved or deleted because it is currently attached as a virtual DVD. A later human-managed relocation may use:

```text
D:\cornerstone\installers\ubuntu\ubuntu-20.04.6-desktop-amd64.iso
```

Only move it after detaching the ISO and after explicit user approval. The VM creation guide uses the current verified path.
