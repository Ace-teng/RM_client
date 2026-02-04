# Placeholder generated from rm_client/proto/referee.proto (Phase 3).
# Regenerate with: gen_proto.bat or: python -m grpc_tools.protoc -I=rm_client/proto --python_out=rm_client/core/protocol/generated rm_client/proto/referee.proto
# This minimal version parses GameStatus (uint32 game_phase, int64 remaining_time_sec) from wire format.

from typing import Optional


def _read_varint(data: bytes, pos: int) -> tuple[int, int]:
    """Read one varint, return (value, new_pos)."""
    result = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
        if shift >= 64:
            break
    return result, pos


class GameStatus:
    """Placeholder for rm_referee.GameStatus (game_phase, remaining_time_sec)."""

    def __init__(self) -> None:
        self.game_phase: int = 0
        self.remaining_time_sec: int = 0

    def MergeFromString(self, data: bytes) -> None:
        """Parse protobuf wire format (field 1: varint, field 2: varint)."""
        pos = 0
        while pos < len(data):
            if pos >= len(data):
                break
            tag = data[pos]
            pos += 1
            if tag == 0x08:  # field 1, varint
                v, pos = _read_varint(data, pos)
                self.game_phase = v
            elif tag == 0x10:  # field 2, varint (int64)
                v, pos = _read_varint(data, pos)
                self.remaining_time_sec = (
                    v if v < 0x8000000000000000 else v - 0x10000000000000000
                )
            else:
                # 未知或其它 wire type：按 varint 跳过一档，避免错位
                if (tag & 0x07) == 0:  # varint
                    _, pos = _read_varint(data, pos)
                else:
                    break

    def SerializeToString(self) -> bytes:
        """Simple serialization for testing."""
        out = bytearray()
        # field 1: tag 0x08, varint
        out.append(0x08)
        v = self.game_phase
        while v > 0x7F:
            out.append((v & 0x7F) | 0x80)
            v >>= 7
        out.append(v)
        # field 2: tag 0x10, varint
        out.append(0x10)
        v = self.remaining_time_sec & 0xFFFFFFFFFFFFFFFF
        while v > 0x7F:
            out.append((v & 0x7F) | 0x80)
            v >>= 7
        out.append(v)
        return bytes(out)
