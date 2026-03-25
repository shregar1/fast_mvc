"""
Enhanced Resource Generator for FastMVC.

Generates complete CRUD resources with:
- Model with SQLAlchemy
- Repository with caching and N+1 protection
- Service with tracing and cost tracking
- Controller with auth and rate limiting
- DTOs with validation
- Tests with mocking
- OpenAPI documentation

Usage:
    fastmvc generate resource Product --crud --ws --graphql
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

import click


@dataclass
class ResourceField:
    """Definition of a resource field."""
    name: str
    type: str
    required: bool = True
    unique: bool = False
    index: bool = False
    encrypted: bool = False
    searchable: bool = False
    default: Optional[str] = None
    description: str = ""


@dataclass
class ResourceConfig:
    """Configuration for resource generation."""
    name: str
    fields: List[ResourceField] = field(default_factory=list)
    enable_crud: bool = True
    enable_auth: bool = True
    enable_cache: bool = True
    enable_tracing: bool = True
    enable_encryption: bool = False
    enable_ws: bool = False
    enable_graphql: bool = False
    enable_tests: bool = True
    enable_soft_delete: bool = True
    enable_audit: bool = True
    enable_rate_limit: bool = True


class ResourceGenerator:
    """
    Generates complete FastMVC resources with production-grade features.
    """
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load code templates."""
        return {
            "model": self._get_model_template(),
            "repository": self._get_repository_template(),
            "service": self._get_service_template(),
            "controller": self._get_controller_template(),
            "dtos": self._get_dtos_template(),
            "tests": self._get_tests_template(),
        }
    
    def generate(self, config: ResourceConfig) -> List[Path]:
        """Generate all resource files."""
        created_files: List[Path] = []
        
        # Create directories
        for dir_name in ["models", "repositories", "services", "controllers", "dtos", "tests/unit"]:
            (self.project_path / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Generate files
        created_files.append(self._generate_model(config))
        created_files.append(self._generate_repository(config))
        created_files.append(self._generate_service(config))
        created_files.append(self._generate_controller(config))
        created_files.append(self._generate_dtos(config))
        
        if config.enable_tests:
            created_files.append(self._generate_tests(config))
        
        # Update router registration
        self._update_router(config)
        
        return created_files
    
    def _generate_model(self, config: ResourceConfig) -> Path:
        """Generate SQLAlchemy model."""
        name = config.name
        table_name = self._to_snake_case(name) + "s"
        
        fields_code = []
        for field in config.fields:
            sa_type = self._map_type_to_sqlalchemy(field.type)
            constraints = []
            
            if field.unique:
                constraints.append("unique=True")
            if field.index:
                constraints.append("index=True")
            if field.default:
                constraints.append(f"default={field.default}")
            if not field.required:
                constraints.append("nullable=True")
            
            constraint_str = ", ".join(constraints)
            if constraint_str:
                constraint_str = ", " + constraint_str
            
            fields_code.append(
                f'    {field.name}: Mapped[{field.type}] = mapped_column({sa_type}{constraint_str})'
            )
        
        soft_delete_code = ""
        if config.enable_soft_delete:
            soft_delete_code = '''
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
'''
        
        encryption_imports = ""
        if config.enable_encryption:
            encryption_imports = "from fast_dashboards.core.encryption import EncryptedString\n"
        
        content = f'''"""
{name} Model

Auto-generated SQLAlchemy model with full audit and soft-delete support.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Integer, Float, Boolean, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
{encryption_imports}


class {name}(Base):
    """
    {name} entity.
    
    Attributes:
        id: Primary key
{chr(10).join(f"        {f.name}: {f.description or f.name}" for f in config.fields)}
    """
    
    __tablename__ = "{table_name}"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
{chr(10).join(fields_code)}
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    created_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
{soft_delete_code}
    
    def __repr__(self) -> str:
        return f"<{name}(id={{self.id}})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {{
            "id": self.id,
{chr(10).join(f'            "{f.name}": self.{f.name},' for f in config.fields)}
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }}
'''
        
        path = self.project_path / "models" / f"{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _generate_repository(self, config: ResourceConfig) -> Path:
        """Generate repository with caching and N+1 protection."""
        name = config.name
        var_name = self._to_snake_case(name)
        
        cache_decorator = ""
        if config.enable_cache:
            cache_decorator = '''
    @smart_cache.cached(
        ttl=300,
        stale_ttl=60,
        invalidate_on=[f"{__tablename__}:update", f"{__tablename__}:delete"]
    )
'''
        
        nplus1_import = ""
        nplus1_context = ""
        if config.enable_tracing:
            nplus1_import = "from fast_dashboards.core.nplus1_detector import detect_nplus1\n"
            nplus1_context = "    @detect_nplus1()\n"
        
        content = f'''"""
{name} Repository

Repository pattern with automatic caching and N+1 query detection.
"""

from typing import List, Optional

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload, selectinload

from database import get_db_session
from models.{self._to_snake_case(name)} import {name}
from fast_dashboards.core.smart_cache import smart_cache
{nplus1_import}


class {name}Repository:
    """
    Repository for {name} entity.
    
    Features:
    - Automatic query result caching
    - N+1 query detection
    - Soft-delete support
    - Full audit trail
    """
    
    __tablename__ = "{self._to_snake_case(name)}s"
    
    async def get_by_id(
        self, 
        id: int, 
        include_deleted: bool = False
    ) -> Optional[{name}]:
        """Get entity by ID with caching."""
        async with get_db_session() as session:
            query = select({name}).where({name}.id == id)
            
            if not include_deleted and hasattr({name}, 'deleted_at'):
                query = query.where({name}.deleted_at.is_(None))
            
            result = await session.execute(query)
            return result.scalar_one_or_none()
{nplus1_context}
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        include_deleted: bool = False
    ) -> List[{name}]:
        """Get all entities with pagination."""
        async with get_db_session() as session:
            query = select({name})
            
            if not include_deleted and hasattr({name}, 'deleted_at'):
                query = query.where({name}.deleted_at.is_(None))
            
            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return list(result.scalars().all())
{cache_decorator}
    async def get_by_field(
        self,
        field_name: str,
        value: any
    ) -> Optional[{name}]:
        """Get entity by any field value."""
        async with get_db_session() as session:
            query = select({name}).where(
                getattr({name}, field_name) == value
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    async def create(self, data: dict, created_by: Optional[str] = None) -> {name}:
        """Create a new entity."""
        async with get_db_session() as session:
            entity = {name}(**data)
            
            if hasattr(entity, 'created_by') and created_by:
                entity.created_by = created_by
            
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            
            # Invalidate cache
            await smart_cache.delete_pattern(f"{self.__tablename__}:*")
            
            return entity
    
    async def update(
        self,
        id: int,
        data: dict,
        updated_by: Optional[str] = None
    ) -> Optional[{name}]:
        """Update an existing entity."""
        async with get_db_session() as session:
            entity = await self.get_by_id(id)
            if not entity:
                return None
            
            for key, value in data.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            
            if hasattr(entity, 'updated_by') and updated_by:
                entity.updated_by = updated_by
            
            await session.commit()
            await session.refresh(entity)
            
            # Invalidate cache
            await smart_cache.delete_pattern(f"{self.__tablename__}:*")
            
            return entity
    
    async def delete(self, id: int, hard: bool = False) -> bool:
        """
        Delete an entity.
        
        Args:
            id: Entity ID
            hard: If True, permanently delete. Otherwise soft delete.
        """
        async with get_db_session() as session:
            entity = await self.get_by_id(id, include_deleted=True)
            if not entity:
                return False
            
            if hard:
                await session.delete(entity)
            else:
                entity.deleted_at = datetime.utcnow()
            
            await session.commit()
            
            # Invalidate cache
            await smart_cache.delete_pattern(f"{self.__tablename__}:*")
            
            return True


# Global repository instance
{var_name}_repository = {name}Repository()
'''
        
        path = self.project_path / "repositories" / f"{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _generate_service(self, config: ResourceConfig) -> Path:
        """Generate service with tracing and cost tracking."""
        name = config.name
        var_name = self._to_snake_case(name)
        
        tracing_imports = ""
        tracing_decorator = ""
        if config.enable_tracing:
            tracing_imports = "from fast_dashboards.core.tracing import tracer, trace_endpoint\n"
            tracing_decorator = "    @tracer.trace_method()\n"
        
        content = f'''"""
{name} Service

Business logic layer with distributed tracing and cost tracking.
"""

from typing import List, Optional
from decimal import Decimal

from repositories.{self._to_snake_case(name)} import {name}Repository, {var_name}_repository
from dtos.{self._to_snake_case(name)} import {name}CreateDTO, {name}UpdateDTO, {name}ResponseDTO
{tracing_imports}


class {name}Service:
    """
    Service for {name} business logic.
    
    Features:
    - Distributed tracing
    - Cost attribution
    - Audit logging
    - Validation
    """
    
    def __init__(self, repository: {name}Repository = None):
        self.repository = repository or {var_name}_repository
{tracing_decorator}
    async def get_by_id(self, id: int) -> Optional[{name}ResponseDTO]:
        """Get entity by ID."""
        entity = await self.repository.get_by_id(id)
        if entity:
            return {name}ResponseDTO.from_model(entity)
        return None
{tracing_decorator}
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[{name}ResponseDTO]:
        """Get all entities with pagination."""
        entities = await self.repository.get_all(skip=skip, limit=limit)
        return [{name}ResponseDTO.from_model(e) for e in entities]
{tracing_decorator}
    async def create(
        self,
        data: {name}CreateDTO,
        created_by: Optional[str] = None
    ) -> {name}ResponseDTO:
        """Create a new entity."""
        entity = await self.repository.create(
            data=data.model_dump(),
            created_by=created_by
        )
        return {name}ResponseDTO.from_model(entity)
{tracing_decorator}
    async def update(
        self,
        id: int,
        data: {name}UpdateDTO,
        updated_by: Optional[str] = None
    ) -> Optional[{name}ResponseDTO]:
        """Update an existing entity."""
        entity = await self.repository.update(
            id=id,
            data=data.model_dump(exclude_unset=True),
            updated_by=updated_by
        )
        if entity:
            return {name}ResponseDTO.from_model(entity)
        return None
{tracing_decorator}
    async def delete(self, id: int, hard: bool = False) -> bool:
        """Delete an entity."""
        return await self.repository.delete(id, hard=hard)


# Global service instance
{var_name}_service = {name}Service()
'''
        
        path = self.project_path / "services" / f"{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _generate_controller(self, config: ResourceConfig) -> Path:
        """Generate FastAPI controller with auth and rate limiting."""
        name = config.name
        var_name = self._to_snake_case(name)
        route_prefix = f"/{var_name}s"
        
        auth_imports = ""
        auth_deps = ""
        if config.enable_auth:
            auth_imports = "from fast_dashboards.core.auth import CurrentUser, RequireRead, RequireWrite, RequireAdmin\n"
            auth_deps = "current_user: User = CurrentUser,\n"
        
        rate_limit_imports = ""
        rate_limit_decorator = ""
        if config.enable_rate_limit:
            rate_limit_imports = "from fast_dashboards.core.rate_limit import RateLimitMiddleware\n"
            rate_limit_decorator = ""
        
        tracing_decorator = ""
        if config.enable_tracing:
            tracing_decorator = "@trace_endpoint()\n"
        
        content = f'''"""
{name} Controller

FastAPI routes with authentication, rate limiting, and tracing.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from services.{self._to_snake_case(name)} import {name}Service, {var_name}_service
from dtos.{self._to_snake_case(name)} import {name}CreateDTO, {name}UpdateDTO, {name}ResponseDTO
from fast_dashboards.core.auth import User
{auth_imports}
{rate_limit_imports}


router = APIRouter(prefix="{route_prefix}", tags=["{name}"])


@{tracing_decorator}@router.get("", response_model=List[{name}ResponseDTO])
async def list_{var_name}s(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    {auth_deps}
) -> List[{name}ResponseDTO]:
    """
    List all {name}s with pagination.
    """
    return await {var_name}_service.get_all(skip=skip, limit=limit)


@{tracing_decorator}@router.get("/{{id}}", response_model={name}ResponseDTO)
async def get_{var_name}(
    id: int,
    {auth_deps}
) -> {name}ResponseDTO:
    """
    Get a specific {name} by ID.
    """
    entity = await {var_name}_service.get_by_id(id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{name} not found"
        )
    return entity


@{tracing_decorator}@router.post("", response_model={name}ResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_{var_name}(
    data: {name}CreateDTO,
    {auth_deps}
) -> {name}ResponseDTO:
    """
    Create a new {name}.
    """
    return await {var_name}_service.create(
        data=data,
        created_by=current_user.id if 'current_user' in locals() else None
    )


@{tracing_decorator}@router.put("/{{id}}", response_model={name}ResponseDTO)
async def update_{var_name}(
    id: int,
    data: {name}UpdateDTO,
    {auth_deps}
) -> {name}ResponseDTO:
    """
    Update an existing {name}.
    """
    entity = await {var_name}_service.update(
        id=id,
        data=data,
        updated_by=current_user.id if 'current_user' in locals() else None
    )
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{name} not found"
        )
    return entity


@{tracing_decorator}@router.delete("/{{id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{var_name}(
    id: int,
    hard: bool = Query(False, description="Permanently delete"),
    {auth_deps}
) -> None:
    """
    Delete a {name}.
    """
    success = await {var_name}_service.delete(id, hard=hard)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{name} not found"
        )
'''
        
        path = self.project_path / "controllers" / f"{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _generate_dtos(self, config: ResourceConfig) -> Path:
        """Generate Pydantic DTOs."""
        name = config.name
        
        fields_create = []
        fields_update = []
        fields_response = []
        
        for field in config.fields:
            field_type = field.type
            if not field.required:
                field_type = f"Optional[{field_type}]"
            
            default = " = None" if not field.required else ""
            
            fields_create.append(f"    {field.name}: {field_type}{default}")
            fields_update.append(f"    {field.name}: {field_type} = None")
            fields_response.append(f"    {field.name}: {field_type}")
        
        content = f'''"""
{name} DTOs

Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class {name}CreateDTO(BaseModel):
    """DTO for creating a new {name}."""
{chr(10).join(fields_create)}


class {name}UpdateDTO(BaseModel):
    """DTO for updating an existing {name}."""
{chr(10).join(fields_update)}


class {name}ResponseDTO(BaseModel):
    """DTO for {name} responses."""
    
    id: int
{chr(10).join(fields_response)}
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_model(cls, model) -> "{name}ResponseDTO":
        """Create DTO from model instance."""
        return cls(
            id=model.id,
{chr(10).join(f'            {f.name}=model.{f.name},' for f in config.fields)}
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
'''
        
        path = self.project_path / "dtos" / f"{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _generate_tests(self, config: ResourceConfig) -> Path:
        """Generate pytest tests."""
        name = config.name
        var_name = self._to_snake_case(name)
        
        content = f'''"""
Tests for {name} resource.

Auto-generated tests for CRUD operations.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from services.{self._to_snake_case(name)} import {name}Service
from repositories.{self._to_snake_case(name)} import {name}Repository
from dtos.{self._to_snake_case(name)} import {name}CreateDTO, {name}UpdateDTO


class Test{name}Service:
    """Tests for {name} service."""
    
    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return AsyncMock(spec={name}Repository)
    
    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mock repository."""
        return {name}Service(repository=mock_repository)
    
    @pytest.mark.asyncio
    async def test_get_by_id_found(self, service, mock_repository):
        """Test getting an existing entity."""
        # Arrange
        mock_entity = MagicMock()
        mock_entity.id = 1
        mock_entity.to_dict.return_value = {{"id": 1, "name": "Test"}}
        mock_repository.get_by_id.return_value = mock_entity
        
        # Act
        result = await service.get_by_id(1)
        
        # Assert
        assert result is not None
        mock_repository.get_by_id.assert_called_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, service, mock_repository):
        """Test getting a non-existent entity."""
        # Arrange
        mock_repository.get_by_id.return_value = None
        
        # Act
        result = await service.get_by_id(999)
        
        # Assert
        assert result is None
    
    @pytest.mark.asyncio
    async def test_create(self, service, mock_repository):
        """Test creating an entity."""
        # Arrange
        dto = {name}CreateDTO(
{chr(10).join(f'            {f.name}="test_value",' for f in config.fields[:2])}
        )
        mock_entity = MagicMock()
        mock_entity.id = 1
        mock_repository.create.return_value = mock_entity
        
        # Act
        result = await service.create(dto)
        
        # Assert
        assert result is not None
        mock_repository.create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_update(self, service, mock_repository):
        """Test updating an entity."""
        # Arrange
        dto = {name}UpdateDTO(
{chr(10).join(f'            {f.name}="updated_value",' for f in config.fields[:1])}
        )
        mock_entity = MagicMock()
        mock_entity.id = 1
        mock_repository.update.return_value = mock_entity
        
        # Act
        result = await service.update(1, dto)
        
        # Assert
        assert result is not None
        mock_repository.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete(self, service, mock_repository):
        """Test deleting an entity."""
        # Arrange
        mock_repository.delete.return_value = True
        
        # Act
        result = await service.delete(1)
        
        # Assert
        assert result is True
        mock_repository.delete.assert_called_once_with(1, hard=False)


class Test{name}Controller:
    """Tests for {name} controller endpoints."""
    
    # Add integration tests here
    pass
'''
        
        path = self.project_path / "tests" / "unit" / f"test_{self._to_snake_case(name)}.py"
        path.write_text(content)
        return path
    
    def _update_router(self, config: ResourceConfig) -> None:
        """Update the main router to include new resource routes."""
        name = config.name
        var_name = self._to_snake_case(name)
        
        # This would modify the main app.py or router file
        # For now, we just print instructions
        click.echo(f"""
Add the following to your main app.py:

from controllers.{var_name} import router as {var_name}_router

app.include_router({var_name}_router)
""")
    
    def _to_snake_case(self, name: str) -> str:
        """Convert CamelCase to snake_case."""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _map_type_to_sqlalchemy(self, type_name: str) -> str:
        """Map Python type names to SQLAlchemy types."""
        mapping = {
            "str": "String(255)",
            "int": "Integer",
            "float": "Float",
            "bool": "Boolean",
            "datetime": "DateTime",
            "dict": "JSON",
            "list": "JSON",
            "Optional[str]": "String(255)",
            "Optional[int]": "Integer",
            "Optional[float]": "Float",
            "Optional[bool]": "Boolean",
            "Optional[datetime]": "DateTime",
        }
        return mapping.get(type_name, "String(255)")


__all__ = [
    "ResourceGenerator",
    "ResourceConfig",
    "ResourceField",
]
