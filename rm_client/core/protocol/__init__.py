# protocol: 协议层，Protobuf 反序列化、Topic 分发、图传包头解析，§4.2
from rm_client.core.protocol.referee_parser import parse_referee_message

__all__ = ["parse_referee_message"]
