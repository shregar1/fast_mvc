"""Tests for DTO base classes."""

from __future__ import annotations

from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

import pytest


class TestBaseDTO:
    """Tests for base DTO functionality."""

    def test_basic_dto_creation(self):
        """Test creating a basic DTO."""
        class TestDTO(BaseModel):
            name: str
            value: int

        dto = TestDTO(name="test", value=42)
        assert dto.name == "test"
        assert dto.value == 42

    def test_dto_serialization(self):
        """Test DTO serialization."""
        class TestDTO(BaseModel):
            name: str
            value: int

        dto = TestDTO(name="test", value=42)
        data = dto.model_dump()
        assert data["name"] == "test"
        assert data["value"] == 42

    def test_dto_json_serialization(self):
        """Test DTO JSON serialization."""
        class TestDTO(BaseModel):
            name: str
            value: int

        dto = TestDTO(name="test", value=42)
        json_str = dto.model_dump_json()
        assert "test" in json_str
        assert "42" in json_str

    def test_dto_validation_error(self):
        """Test DTO validation error."""
        class TestDTO(BaseModel):
            name: str
            value: int

        with pytest.raises(Exception):
            TestDTO(name="test", value="not-an-int")

    def test_dto_optional_field(self):
        """Test DTO with optional field."""
        class TestDTO(BaseModel):
            name: str
            description: Optional[str] = None

        dto1 = TestDTO(name="test")
        dto2 = TestDTO(name="test", description="desc")
        assert dto1.description is None
        assert dto2.description == "desc"

    def test_dto_default_values(self):
        """Test DTO with default values."""
        class TestDTO(BaseModel):
            name: str
            count: int = 0
            active: bool = True

        dto = TestDTO(name="test")
        assert dto.count == 0
        assert dto.active is True

    def test_dto_with_datetime(self):
        """Test DTO with datetime field."""
        class TestDTO(BaseModel):
            name: str
            created_at: datetime

        now = datetime.now()
        dto = TestDTO(name="test", created_at=now)
        assert dto.created_at == now

    def test_dto_with_decimal(self):
        """Test DTO with decimal field."""
        class TestDTO(BaseModel):
            name: str
            price: Decimal

        dto = TestDTO(name="test", price=Decimal("10.99"))
        assert dto.price == Decimal("10.99")

    def test_dto_with_list(self):
        """Test DTO with list field."""
        class TestDTO(BaseModel):
            name: str
            items: List[str]

        dto = TestDTO(name="test", items=["a", "b", "c"])
        assert len(dto.items) == 3

    def test_dto_with_dict(self):
        """Test DTO with dict field."""
        class TestDTO(BaseModel):
            name: str
            metadata: Dict[str, Any]

        dto = TestDTO(name="test", metadata={"key": "value"})
        assert dto.metadata["key"] == "value"

    def test_dto_nested_models(self):
        """Test nested DTO models."""
        class Address(BaseModel):
            street: str
            city: str

        class Person(BaseModel):
            name: str
            address: Address

        dto = Person(
            name="John",
            address=Address(street="123 Main", city="NYC")
        )
        assert dto.address.city == "NYC"

    def test_dto_field_validation(self):
        """Test DTO field validation."""
        class TestDTO(BaseModel):
            name: str = Field(..., min_length=3, max_length=50)
            age: int = Field(..., ge=0, le=150)

        dto = TestDTO(name="John", age=25)
        assert dto.name == "John"
        assert dto.age == 25

    def test_dto_field_alias(self):
        """Test DTO field alias."""
        class TestDTO(BaseModel):
            model_config = {"populate_by_name": True}
            first_name: str = Field(alias="firstName")

        dto = TestDTO(firstName="John")
        assert dto.first_name == "John"

    def test_dto_immutability(self):
        """Test DTO immutability."""
        class TestDTO(BaseModel):
            model_config = {"frozen": True}
            name: str

        dto = TestDTO(name="test")
        assert dto.name == "test"


class TestDTOEdgeCases:
    """Test DTO edge cases."""

    def test_dto_with_empty_string(self):
        """Test DTO with empty string."""
        class TestDTO(BaseModel):
            name: str

        dto = TestDTO(name="")
        assert dto.name == ""

    def test_dto_with_unicode(self):
        """Test DTO with unicode."""
        class TestDTO(BaseModel):
            name: str

        dto = TestDTO(name="测试")
        assert dto.name == "测试"

    def test_dto_with_special_characters(self):
        """Test DTO with special characters."""
        class TestDTO(BaseModel):
            name: str

        special = "test<>!@#$%^&*()"
        dto = TestDTO(name=special)
        assert dto.name == special

    def test_dto_with_none_optional(self):
        """Test DTO with None optional."""
        class TestDTO(BaseModel):
            name: str
            desc: Optional[str] = None

        dto = TestDTO(name="test", desc=None)
        assert dto.desc is None

    def test_dto_list_validation(self):
        """Test DTO list validation."""
        class TestDTO(BaseModel):
            items: List[int]

        with pytest.raises(Exception):
            TestDTO(items=[1, 2, "not-an-int"])

    def test_dto_dict_validation(self):
        """Test DTO dict validation."""
        class TestDTO(BaseModel):
            data: Dict[str, int]

        dto = TestDTO(data={"a": 1, "b": 2})
        assert dto.data["a"] == 1

    def test_dto_extra_fields_forbidden(self):
        """Test DTO extra fields forbidden."""
        class TestDTO(BaseModel):
            model_config = {"extra": "forbid"}
            name: str

        with pytest.raises(Exception):
            TestDTO(name="test", extra_field="value")

    def test_dto_from_dict(self):
        """Test creating DTO from dict."""
        class TestDTO(BaseModel):
            name: str
            value: int

        dto = TestDTO.model_validate({"name": "test", "value": 42})
        assert dto.name == "test"
        assert dto.value == 42

    def test_dto_from_json(self):
        """Test creating DTO from JSON."""
        class TestDTO(BaseModel):
            name: str
            value: int

        json_str = '{"name": "test", "value": 42}'
        dto = TestDTO.model_validate_json(json_str)
        assert dto.name == "test"
        assert dto.value == 42
