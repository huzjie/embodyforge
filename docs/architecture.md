# 架构

```
                        +---------------------+
 observation/scene ---> | embodied.foundation | ---> motion primitive
                        |  (perception+action)|
                        +----------+----------+
                                   | skill
        +-----------------+--------+--------+-----------------+
        |                 |                 |                 |
   +----v----+      +-----v-----+     +-----v-----+     +-----v-----+
   | gait    |      | choreo    |     | control   |     | orchestra |
   | walk/gen|      | keyframe  |     | PD+ZMP+fall|    | clock/lock |
   +----+----+      +-----+-----+     +-----+-----+     | formation |
        |                 |                 |           | collision |
        +-----------------+-----------------+           +-----------+
                          |
                    +-----v-----+      +--------------+
                    | kinematics| ---> | dynamics CoM |
                    | FK/IK/Jac |      | ZMP / LIPM   |
                    +-----------+      +--------------+
```

数据流：感知 → 选动作原语 → 步态/编舞生成参考关节角 → 运动学算末端/脚位 →
动力学算 CoM/ZMP → 控制保持平衡并检测跌倒；多机层负责时钟同步、相位锁定、编队与防碰撞。
