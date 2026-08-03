# 已核实资料事实

## Linker Hand L6
- 6 主动自由度，11 关节（6 主动 + 5 被动）
- 重量 607 g
- DC 24 V ±10%
- 最大电流 1.4 A
- CAN / RS485
- 官方提供 ROS、ROS2、Python SDK

## 机器人资料包
资料包同时包含两种平台资料，不能仅凭压缩包认定实物型号：

### Julab Mini
- 控制器：Ubuntu 18.04 + ROS Melodic
- 4 轴机械臂
- 机械臂额定负载：500 g
- 因 L6 本体 607 g，若实物是该版本，直接安装会超过机械臂额定负载，属于阻断项。

### Sparrow Pro420
- 控制器：Ubuntu 18.04 + ROS Melodic
- 6 轴 INNFOS 机械臂
- 机械臂额定负载：1.2 kg
- 原三指柔性夹爪重量：0.25 kg
- L6 本体 0.607 kg，尚未计转接板、电缆和被抓物，必须重新核算有效负载。

## 环境策略
- Ubuntu 20.04 + ROS Noetic：用于官方 Linker Hand ROS1 SDK。
- Ubuntu 18.04 + ROS Melodic：用于复合机器人原厂软件兼容验证。
- 两套环境不要混装在同一个系统中，优先创建两台独立 VMware 虚拟机。
