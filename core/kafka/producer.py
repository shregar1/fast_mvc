"""
Kafka producer integration using aiokafka.
"""

from typing import Any

from aiokafka import AIOKafkaProducer

from configurations.kafka import KafkaConfiguration
from start_utils import logger


class KafkaProducer:
    """
    High-level Kafka producer wrapper.
    """

    def __init__(self) -> None:
        cfg = KafkaConfiguration().get_config()
        self._cfg = cfg
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        if not self._cfg.enabled:
            logger.info("Kafka producer not started (disabled in config).")
            return
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._cfg.bootstrap_servers,
        )
        await self._producer.start()
        logger.info("Kafka producer started.")

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()
            logger.info("Kafka producer stopped.")

    async def send(self, topic: str, value: Any) -> None:
        if not self._producer:
            logger.warning("Kafka producer is not running; message dropped.")
            return
        await self._producer.send_and_wait(topic, str(value).encode("utf-8"))

