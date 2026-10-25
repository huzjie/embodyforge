# HTTP API

启动：`python -m embodyforge serve`（默认 `http://127.0.0.1:8322`）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | /health | 健康检查 |
| GET | /v1/models | 声明规模 + 后端列表 |
| POST | /v1/solve | `{"scene_id","skill"}` -> 所选动作原语与是否成功 |
| POST | /v1/step | `{"t","skill"}` -> 一个控制步（CoM/脚位/稳定裕度/是否跌倒） |
