"""
Datastore client implementations for FastMVC.

This package contains concrete implementations of the generic datastore
interfaces defined in `abstractions.datastore` for specific technologies
such as Redis, MongoDB, Cassandra, DynamoDB, Cosmos DB, and ScyllaDB.

All clients are intentionally thin wrappers around the underlying drivers
so that they are easy to extend or replace in user projects.
"""

from .redis_kv import RedisKeyValueStore  # noqa: F401
from .mongo import MongoDocumentStore  # noqa: F401
from .cassandra import CassandraWideColumnStore  # noqa: F401
from .scylla import ScyllaWideColumnStore  # noqa: F401
from .dynamo import DynamoKeyValueStore  # noqa: F401
from .cosmos import CosmosDocumentStore  # noqa: F401
from .elasticsearch import ElasticsearchSearchStore  # noqa: F401

__all__ = [
    "RedisKeyValueStore",
    "MongoDocumentStore",
    "CassandraWideColumnStore",
    "ScyllaWideColumnStore",
    "DynamoKeyValueStore",
    "CosmosDocumentStore",
    "ElasticsearchSearchStore",
]

