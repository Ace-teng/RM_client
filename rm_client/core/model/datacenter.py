"""
DataCenter — 全系统唯一状态源（R-ARCH-002）。

单例、线程安全；提供统一读写接口；支持订阅通知（观察者）。
所有比赛实时状态集中存储于此；UI 与 service 只读写 DataCenter，禁止私有缓存。
见总文档 §4.3。
"""
from __future__ import annotations

import threading
from typing import Any, Callable, Dict, List, Optional

# 类型占位：后续由 protocol/赛事协议 填充
GameState = Any
RobotStates = Dict[str, Any]
Events = List[Any]
VideoFrame = Any
OverlayBoxes = List[Any]
CalibrationResult = Any
LinkStatus = Dict[str, Any]


class DataCenter:
    """
    全局数据中心单例。
    存储：game_state, robot_states, events, video_frame, overlay_boxes, calibration_result, link_status。
    """

    _instance: Optional["DataCenter"] = None
    _lock = threading.Lock()
    _subscribers: List[Callable[[str, Any], None]] = []

    def __new__(cls) -> "DataCenter":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._lock_io = threading.RLock()
        self._game_state: Optional[GameState] = None
        self._robot_states: RobotStates = {}
        self._events: Events = []
        self._video_frame: Optional[VideoFrame] = None
        self._overlay_boxes: OverlayBoxes = []
        self._calibration_result: Optional[CalibrationResult] = None
        self._link_status: LinkStatus = {}
        self._initialized = True

    def _notify(self, key: str, value: Any) -> None:
        for cb in self._subscribers:
            try:
                cb(key, value)
            except Exception:
                pass

    def subscribe(self, callback: Callable[[str, Any], None]) -> None:
        """注册订阅：状态变更时回调 callback(key, value)。"""
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[str, Any], None]) -> None:
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    # ---------- 统一读写接口 ----------

    @property
    def game_state(self) -> Optional[GameState]:
        with self._lock_io:
            return self._game_state

    @game_state.setter
    def game_state(self, value: Optional[GameState]) -> None:
        with self._lock_io:
            self._game_state = value
        self._notify("game_state", value)

    @property
    def robot_states(self) -> RobotStates:
        with self._lock_io:
            return self._robot_states.copy()

    @robot_states.setter
    def robot_states(self, value: RobotStates) -> None:
        with self._lock_io:
            self._robot_states = dict(value)
        self._notify("robot_states", self._robot_states)

    @property
    def events(self) -> Events:
        with self._lock_io:
            return list(self._events)

    @events.setter
    def events(self, value: Events) -> None:
        with self._lock_io:
            self._events = list(value)
        self._notify("events", self._events)

    @property
    def video_frame(self) -> Optional[VideoFrame]:
        with self._lock_io:
            return self._video_frame

    @video_frame.setter
    def video_frame(self, value: Optional[VideoFrame]) -> None:
        with self._lock_io:
            self._video_frame = value
        self._notify("video_frame", value)

    @property
    def overlay_boxes(self) -> OverlayBoxes:
        with self._lock_io:
            return list(self._overlay_boxes)

    @overlay_boxes.setter
    def overlay_boxes(self, value: OverlayBoxes) -> None:
        with self._lock_io:
            self._overlay_boxes = list(value)
        self._notify("overlay_boxes", self._overlay_boxes)

    @property
    def calibration_result(self) -> Optional[CalibrationResult]:
        with self._lock_io:
            return self._calibration_result

    @calibration_result.setter
    def calibration_result(self, value: Optional[CalibrationResult]) -> None:
        with self._lock_io:
            self._calibration_result = value
        self._notify("calibration_result", value)

    @property
    def link_status(self) -> LinkStatus:
        with self._lock_io:
            return dict(self._link_status)

    @link_status.setter
    def link_status(self, value: LinkStatus) -> None:
        with self._lock_io:
            self._link_status = dict(value)
        self._notify("link_status", self._link_status)
