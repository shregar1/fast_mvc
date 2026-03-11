"""
DTO for generic OpenTelemetry (OTel) configuration settings.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class TelemetryConfigurationDTO(BaseModel):
    """
    DTO for OpenTelemetry configuration.
    """

    enabled: bool = False
    exporter: Literal["otlp", "console", "none"] = "otlp"
    endpoint: Optional[str] = None
    protocol: Literal["grpc", "http/protobuf"] = "grpc"
    service_name: str = "fastmvc-api"
    environment: str = "development"

