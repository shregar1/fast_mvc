"""
Example Kafka worker process.

Consume messages from configured Kafka topics and process them.
"""

import asyncio

from core.kafka.consumer import KafkaConsumer
from start_utils import logger


async def handle_message(topic: str, value: bytes) -> None:
    logger.info(f"Kafka message received", topic=topic, value=value.decode("utf-8", "ignore"))


async def main() -> None:
    consumer = KafkaConsumer()
    await consumer.start()
    try:
        await consumer.loop(handle_message)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())

