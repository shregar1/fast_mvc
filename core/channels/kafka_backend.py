"""
Kafka-based implementation of the channels backend (stub).

Requires aiokafka; this module is a placeholder to show the intended
interface and can be fully implemented when Kafka support is enabled.
"""

from typing import Any, AsyncGenerator

from core.channels.base import ChannelBackend


class KafkaChannelBackend(ChannelBackend):
    def __init__(self) -> None:
        # Real implementation would accept producer/consumer instances
        pass

    async def publish(self, topic: str, message: Any) -> None:
        # TODO: Implement using aiokafka.AIOKafkaProducer
        raise NotImplementedError("Kafka backend is not yet implemented.")

    async def subscribe(self, topic: str) -> AsyncGenerator[str, None]:
        # TODO: Implement using aiokafka.AIOKafkaConsumer
        raise NotImplementedError("Kafka backend is not yet implemented.")

