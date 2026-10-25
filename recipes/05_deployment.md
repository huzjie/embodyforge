# 配方：部署上线

1. 容器化用 `Dockerfile`（python:3.11-slim），暴露 8322。
2. K8s 三副本 + Service 即可水平扩展（`deploy/k8s.yaml`）。
3. 边缘设备上优先用 `cpu` 后端，别上 openai/vllm（网络 + 延迟）。
4. 真实机器人接 ROS 用 `integrations/ros_bridge` 的发布/订阅接口替换。
