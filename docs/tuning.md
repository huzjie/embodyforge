# 调参指南

| 参数 | 作用 | 建议区间 |
|---|---|---|
| `control.kp` | CoM 回正刚度 | 100~150（快走取高） |
| `control.kd` | 阻尼 | 8~12 |
| `control.fall_margin` | 跌倒判据 | 0.03（保守）~0.06（宽松） |
| `orchestra.coupling` | 相位锁耦合强度 | 0.3~0.5 |
| `gait.cadence` | 步频 | 1.2~1.8 |
| `embodied.learning_rate` | skill 爬升速率 | 0.2 |

先调 `kp` 再调 `kd`；`coupling` 太大会过冲振荡，太小锁相慢。
