# 先读：WINDOWS_HANDOFF_NOT_FOUND 修复

出现该错误的原因：在 Windows 中直接运行了 Ubuntu 阶段提示词，但 Windows 阶段项目目录尚未创建。

正确顺序：

1. 将本目录完整复制/解压到：
   `D:\cornerstone\codex\linkerhand_composite_robot`
2. 确认原始资料位于：
   `D:\cornerstone\技术文档`
3. 在 Windows Codex 中执行：
   `11_handoff\WINDOWS_CODEX_RECOVERY_PROMPT.md`
4. Windows 阶段完成并输出 `WINDOWS_HANDOFF_READY` 后，再启动 Ubuntu 虚拟机。
5. Ubuntu 20.04 中执行 `11_handoff\UBUNTU20_NEXT_PROMPT.md`。
6. Ubuntu 18.04 机器人兼容环境后续按 `11_handoff\UBUNTU18_ROBOT_PLAN.md` 建立。

不要在 Windows PowerShell 中执行 Linux/ROS 安装命令。
