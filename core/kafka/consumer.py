"""
Kafka consumer integration using aiokafka.
"""

from typing import Any, Awaitable, Callable

from aiokafka import AIOKafkaConsumer

from configurations.kafka import KafkaConfiguration
from start_utils import logger


class KafkaConsumer:
    """
    High-level Kafka consumer wrapper.
    """

    def __init__(self) -> None:
        cfg = KafkaConfiguration().get_config()
        self._cfg = cfg
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        if not self._cfg.enabled:
            logger.info("Kafka consumer not started (disabled in config).")
            return
        self._consumer = AIOKafkaConsumer(
            *self._cfg.topics,
            bootstrap_servers=self._cfg.bootstrap_servers,
            group_id=self._cfg.group_id,
            enable_auto_commit=self._cfg.enable_auto_commit,
        )
        await self._consumer.start()
        logger.info("Kafka consumer started.")

    async def stop(self) -> None:
        if self._consumer:
            await self._consumer.stop()
            logger.info("Kafka consumer stopped.")

    async def loop(self, handler: Callable[[str, bytes], Awaitable[None]]) -> None:
        """
        Consume messages in a loop and dispatch to handler(topic, value).
        """
        if not self._consumer:
            logger.warning("Kafka consumer is not running; loop exited.")
            return
        async for msg in self._consumer:
            await handler(msg.topic, msg.value)

