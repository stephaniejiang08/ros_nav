# Official SDK Commit Pins

Checked on Windows at: `2026-08-03T11:04:37+08:00`

The repositories were cloned from the exact URLs below into `D:\cornerstone\codex\linkerhand_composite_robot\03_linkerhand_vendor`. They were not run and no dependencies were installed.

| SDK | URL | Branch | HEAD commit | Commit time | Subject | Worktree |
|---|---|---|---|---|---|---|
| ROS1 | `https://github.com/linker-bot/linkerhand-ros-sdk.git` | `main` | `2aa379cd11562d953f8b449561107b58c120676e` | `2026-02-08T14:29:57+08:00` | `Update Topic-Reference.md` | CLEAN |
| Python | `https://github.com/linker-bot/linkerhand-python-sdk.git` | `main` | `fbec1057e5320918f634fff103835d9aaa0a2269` | `2026-07-15T17:23:17+08:00` | `Update setting.yaml` | CLEAN |
| ROS2 | `https://github.com/linker-bot/linkerhand-ros2-sdk.git` | `main` | `f63bf61a03f97465844c952608e744c09bff7a2f` | `2026-07-29T11:02:39+08:00` | `O6支持手掌传感器` | CLEAN |

## Required checkout for Ubuntu 20.04 phase

The ROS1 build must use exactly:

```text
2aa379cd11562d953f8b449561107b58c120676e
```

Do not silently update to a later `main`. If a later commit is proposed, stop, record the new commit, review its diff, and obtain user approval before changing the pin.

## Static audit facts at the pinned ROS1 commit

- Documented platform: Ubuntu 20.04, ROS Noetic, Python 3.8; `doc/hardware_settings.md` explicitly names Python 3.8.10.
- L6 supported over CAN and RS485.
- Documented SocketCAN bitrate: 1,000,000 bit/s.
- L6 six-value order: thumb flexion, thumb yaw/lateral, index, middle, ring, pinky.
- `find_linker_hand.sh` transmits CAN frames via `cansend` and is prohibited for read-only enumeration.
- Vendor configuration includes unsafe example practices (stored password sample and broad serial permissions); do not copy those practices into project configuration.

