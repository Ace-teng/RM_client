"""
Phase 5 占位数据 — 向 DataCenter 写入 demo robot_states，便于态势图展示。

协议接入后由 protocol 层写入真实数据，本模块可停用或仅用于离线演示。
"""
from rm_client.core.model.datacenter import DataCenter


def inject_demo_robot_states() -> None:
    """写入占位 robot_states，格式：{robot_id: {x, y, hp, team}}，x/y 为 0～1 归一化坐标。"""
    dc = DataCenter()
    dc.robot_states = {
        "red_1": {"x": 0.25, "y": 0.5, "hp": 600, "team": "red"},
        "red_2": {"x": 0.35, "y": 0.35, "hp": 600, "team": "red"},
        "blue_1": {"x": 0.75, "y": 0.5, "hp": 600, "team": "blue"},
        "blue_2": {"x": 0.65, "y": 0.65, "hp": 450, "team": "blue"},
    }
