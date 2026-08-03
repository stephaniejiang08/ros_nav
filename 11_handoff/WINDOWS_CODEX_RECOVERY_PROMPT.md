你正在 Windows PowerShell 环境中修复“WINDOWS_HANDOFF_NOT_FOUND”。

目标：只在 D 盘创建完整的 Windows 交接目录，审计用户已有资料和官方 SDK；本阶段不安装 Linux、不安装 ROS、不连接硬件、不运行机器人或灵巧手。

【唯一项目根目录】
D:\cornerstone\codex\linkerhand_composite_robot

【原始资料优先目录】
D:\cornerstone\技术文档

【D 盘临时目录】
D:\cornerstone\codex\_temp

先执行并验证：
$env:TEMP='D:\cornerstone\codex\_temp'
$env:TMP='D:\cornerstone\codex\_temp'
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
New-Item -ItemType Directory -Force -Path 'D:\cornerstone\codex\linkerhand_composite_robot' | Out-Null
Set-Location 'D:\cornerstone\codex\linkerhand_composite_robot'

禁止把项目文件写到 C 盘、桌面、下载、文档、OneDrive、用户目录或系统 TEMP。
如果任何待创建的项目路径不在 D:\cornerstone 下，立即停止。

一、保留已有文件
- 不删除或覆盖本目录已有 README_FIRST.md、VERIFIED_FACTS.md 和本提示词。
- 不修改 D:\cornerstone\技术文档 中原始文件。

二、查找资料
递归查找 D:\cornerstone 下列文件，不要求文件名完全一致：
- Linker Hand L6 产品手册 PDF
- 哈工大（合肥）创新研究院复合机器人 ZIP
- Julab Mini 文档/源码
- Sparrow Pro420 文档

若资料不在 D:\cornerstone\技术文档，但在 D:\cornerstone 其他目录，记录真实路径并继续。
若完全找不到，创建 01_document_audit\MISSING_SOURCE_FILES.md 后停止。

三、创建目录
创建：
00_source_manifest
01_document_audit
02_robot_vendor\extracted
03_linkerhand_vendor
04_robot_melodic_ws\src
05_linkerhand_noetic_ws\src
06_integration
07_scripts\windows
07_scripts\ubuntu20
07_scripts\ubuntu18
08_tests
09_design\mechanical
09_design\electrical
09_design\software
10_logs
11_handoff
_temp

四、资料清单与解压
- 对找到的原始 PDF/ZIP/DOCX 计算 SHA256，写入 00_source_manifest\SOURCE_MANIFEST.md。
- 将复合机器人 ZIP 解压到 02_robot_vendor\extracted，继续解压其中 julab_mini-master-2.zip。
- 不运行压缩包中的 EXE、脚本、ROS 节点或 demo。
- 识别两套机器人资料：Julab Mini 与 Sparrow Pro420，不得混为同一型号。

五、审计关键事实
从文档和源码提取并写入：
01_document_audit\ROBOT_AUDIT.md
01_document_audit\LINKERHAND_AUDIT.md
01_document_audit\COMPATIBILITY_MATRIX.md
01_document_audit\MISSING_INFORMATION.md

必须明确记录：
- Julab Mini：Ubuntu 18.04 + ROS Melodic；4轴机械臂；额定负载500g。
- Sparrow Pro420：Ubuntu 18.04 + ROS Melodic；6轴INNFOS机械臂；额定负载1.2kg；原夹爪0.25kg、TTL串口。
- Linker Hand L6：607g、24V±10%、最大1.4A、CAN/RS485。
- 若实物是 Julab Mini 500g 机械臂，L6 本体已超载，标记 BLOCKED。
- 若实物是 Sparrow Pro420，计算：1200g - 607g = 593g；该余量还要扣除转接板、电缆和被抓物，标记“需实物确认与负载核算”。
- 左手/右手、是否带触觉、USB-CAN型号、真实机器人型号均标记 UNKNOWN，不能猜。

六、审计官方 SDK
在 03_linkerhand_vendor 下克隆：
https://github.com/linker-bot/linkerhand-ros-sdk.git
https://github.com/linker-bot/linkerhand-python-sdk.git
https://github.com/linker-bot/linkerhand-ros2-sdk.git

只克隆和读取，不运行，不安装依赖。
对每个仓库记录：URL、分支、HEAD commit hash、检查时间。
重点确认 ROS1 SDK 当前要求 Ubuntu 20.04 / ROS Noetic / Python 3.8.10，以及 L6、CAN、RS485、1Mbps CAN 配置和 L6 六个控制量顺序。

七、生成最小交接文件
创建：
11_handoff\WINDOWS_HANDOFF_SUMMARY.md
11_handoff\SDK_COMMITS.md
11_handoff\FILES_TO_COPY_TO_LINUX.md
11_handoff\UBUNTU20_CODEX_PROMPT.md
11_handoff\UBUNTU18_ROBOT_VM_PLAN.md
NEXT_ACTIONS.md

WINDOWS_HANDOFF_SUMMARY.md 必须包含：
- 原始资料真实路径
- 实际机器人型号仍待人工确认
- 两种机械臂负载风险
- 三个官方 SDK commit hash
- 推荐先建 Ubuntu20.04/Noetic 手部环境，再建 Ubuntu18.04/Melodic 机器人兼容环境
- 当前没有执行任何硬件运动

UBUNTU20_CODEX_PROMPT.md 只允许在 Ubuntu 20.04 虚拟机中运行，必须先检测 /etc/os-release；若不是 20.04 立即停止。

八、Git
如未初始化，初始化本地 Git 仓库。
不得修改 Git 全局配置，不得推送远程。
提交信息：
phase0: create windows handoff for robot and linkerhand integration

九、完成检查
确认以下文件存在：
D:\cornerstone\codex\linkerhand_composite_robot\11_handoff\WINDOWS_HANDOFF_SUMMARY.md
D:\cornerstone\codex\linkerhand_composite_robot\11_handoff\SDK_COMMITS.md
D:\cornerstone\codex\linkerhand_composite_robot\11_handoff\UBUNTU20_CODEX_PROMPT.md

最后打印：
WINDOWS_HANDOFF_READY
PROJECT_ROOT=D:\cornerstone\codex\linkerhand_composite_robot
SUMMARY=D:\cornerstone\codex\linkerhand_composite_robot\11_handoff\WINDOWS_HANDOFF_SUMMARY.md
UBUNTU_PROMPT=D:\cornerstone\codex\linkerhand_composite_robot\11_handoff\UBUNTU20_CODEX_PROMPT.md
HARDWARE_MOTION_EXECUTED=FALSE

执行到此停止，不进入 Linux 安装。
