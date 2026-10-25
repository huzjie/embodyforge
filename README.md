# embodyforge

**具身智能人形机器人协同运动控制引擎** —— 纯 Python 零依赖参考实现。

拆解 2026-10-24 智元「110 台远征 A3 全尺寸人形机器人同时跳舞」吉尼斯世界纪录背后的
技术栈，以及业内所预判的「具身智能 2026-2028 GPT3 时刻」：运动学、动力学、平衡控制、
节拍编舞、多机协同、具身基础模型，六个可独立调优的组件，一套共享的确定性 oracle。

> 本项目是**可运行的参考实现**，不是示例片段：`python -m embodyforge doctor` 自检、
> `bench` 跑 5 项基准、`serve` 起 HTTP 服务、`train` 演示 skill 0.5→1.0 的单调训练。

## 一句话讲清原理

人形机器人「同时跳舞」= 三件事的叠加：

1. **单机站得稳**（动力学）：零力矩点 ZMP 落在双脚支撑多边形内。用线性倒立摆模型
   LIPM 前推 CoM 轨迹，ZMP 预览控制器把指令 ZMP 夹回多边形。
2. **节拍锁得齐**（分布式）：110 台机器各有晶振漂移，用 NTP 式逻辑时钟同步 +
   Kuramoto 弱耦合振子把相位锁到同一个节拍。
3. **动作学得会**（具身智能）：感知 → 选运动原语 → 查技能库，用 RL 信号让成功率
   从随机基线单调爬到最优。

## 六个组件

| 组件 | 目录 | 干什么 |
|---|---|---|
| 运动学 | `kinematics/` | 正/逆运动学、数值雅可比、DLS 逆解（腿 6-DoF / 臂 7-DoF） |
| 动力学 | `dynamics/` | CoM、ZMP、LIPM 倒立摆 |
| 步态 | `gait/` | 相位机、足迹规划、步行周期生成器 |
| 控制 | `control/` | PD 力矩、ZMP 预览平衡、跌倒检测 |
| 编舞 | `choreo/` | 关键帧动作库、slerp 插值、节拍同步舞蹈 |
| 协同 | `orchestra/` | 逻辑时钟、Kuramoto 相位锁、编队、防碰撞 |
| 具身 | `embodied/` | 感知编码器、动作头、技能库、基础模型 |

## 快速开始

```bash
python -m embodyforge doctor     # 自检：链条/FK/IK/模型前向/5 后端
python -m embodyforge bench      # 5 项基准（全单调）
python -m embodyforge train      # skill 0.5 -> 1.0 单调训练
python -m embodyforge demo       # 一段编舞 + 一个 IK 求解
python -m embodyforge serve      # HTTP API（/health /v1/models /v1/solve /v1/step）
python -m unittest discover -s tests -t .   # 全量单测
```

## 基准（实测）

skill 是贯穿全项目的「策略质量」标量：0.5 = 随机/未训练，1.0 = 完美。每项学习基准
从随机基线单调爬向最优，曲线干净可复现。

| 基准 | 指标 | skill=0.5 | skill=1.0 | 单调 |
|---|---|---|---|---|
| balance | ZMP 稳定裕度 | 0.200 | 0.400 | ✅ |
| sync | Kuramoto 序参量 r | 0.561 | 0.749 | ✅ |
| gait | 行走稳定性 | 0.495 | 1.000 | ✅ |
| skill_recall | 技能召回 recall@1 | 0.105 | 1.000 | ✅ |
| speedup | 多机协同加速比 | 6.67× | 8.00× | ✅ |

## 可复用思路（工程干货）

1. **ZMP 是平衡的「单一真值」**：不要另造经验规则，跌倒检测、稳定性基准全围绕
   「ZMP 是否在多边形内 + 到边界距离」展开。LIPM 的 CoM 动力学是
   `x_ddot = (g/h)(x - zmp_x)`，是线性系统，所以预览控制能解析前推。

2. **多机协同是分布式共识问题**：相位对齐用 Kuramoto
   `dθ_i/dt = ω_i + K/N Σ sin(θ_j - θ_i)`，序参量 r 是锁相程度的单值度量；
   时钟同步用均值（NTP 思想）。把成熟的分布式工具搬到机器人上，比从零造协议快。

3. **数值雅可比 + DLS 逆解够用**：任意旋转关节链的解析雅可比代码量远大于参考价值，
   中心差分 `J[i][j] = (ee_i(θ+ε) - ee_i(θ-ε))/2ε` + 阻尼最小二乘
   `dq = J^T(JJ^T+λ²I)^-1(target-ee)` 就稳定收敛。

4. **训练信号单调趋 1**：`skill += lr(1-skill)` 恒正几何爬升；打分
   `boost=(skill-0.5)*2`，skill=0.5 时 boost=0（随机基线）、1.0 时 boost=1（恒正确）。
   绝不用「对 +1 错 -1」的随机游走（会被压到 0）。

5. **声明规模与实例化解耦**：110 台 40-DoF 真实人形机器人纯 Python 会卡死，config 分
   `declared`（口径）与实例化 tiny 结构两层。

6. **确定性随机 md5(key)**：所有 mock/oracle/基准共享同一 md5 种子，输出可复现。

## 目录结构

```
embodyforge/            # 主包（kinematics/dynamics/gait/control/choreo/orchestra/embodied/backends/bench/serving）
tests/                  # 单测
examples/               # 10 个可运行示例
docs/ prompts/ recipes/ # 文档 / 提示词模板 / 调参配方
deploy/ .github/        # Docker / K8s / Helm / CI
```

## 许可

MIT
