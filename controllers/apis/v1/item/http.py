"""Shared FastAPI/JSON helpers for the Item API (DRY response and error handling)."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any, TypeVar

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from abstractions.result import Result
from constants.http_header import HttpHeader
from dtos.responses.item import (
    ItemListResponseDTO,
    ItemResponseDTO,
    ItemStatsResponseDTO,
)
from models.item import Item

_TVal = TypeVar("_TVal")


class ItemHttpResponseBuilder:
    """Builder class for Item API HTTP responses."""

    @staticmethod
    def item_ref_headers(
        *,
        body_reference: str | None,
        http_request: Request | None,
    ) -> dict[str, str]:
        """Prefer body ``reference_urn``; else echo ``x-reference-urn`` from the request."""
        ref = body_reference
        if ref is None and http_request is not None:
            ref = http_request.headers.get(HttpHeader.X_REFERENCE_URN)
        return HttpHeader().get_reference_urn_header(reference_urn=ref)

    @staticmethod
    def raise_bad_request_if_failure(result: Result[Any, Any]) -> None:
        """Raise HTTP 400 if result is a failure."""
        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

    @classmethod
    def _success_payload(cls, result: Result[_TVal, Any]) -> _TVal:
        """Narrow a successful ``Result`` to its value (400 if failure)."""
        cls.raise_bad_request_if_failure(result)
        assert result.value is not None
        return result.value

    @staticmethod
    def raise_unprocessable_if_dto_invalid(dto: Any) -> None:
        """Raise HTTP 422 if DTO validation fails."""
        is_valid, errors = dto.validate()
        if not is_valid:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"errors": errors},
            )

    @classmethod
    def json_item(
        cls,
        entity: Item,
        http_request: Request | None,
        *,
        reference_urn: str | None = None,
        status_code: int = HTTPStatus.OK,
    ) -> JSONResponse:
        """Build JSON response for a single item."""
        dto = ItemResponseDTO.from_entity(entity, reference_urn=reference_urn)
        return JSONResponse(
            status_code=status_code,
            content=dto.to_dict(),
            headers=cls.item_ref_headers(
                body_reference=reference_urn, http_request=http_request
            ),
        )

    @classmethod
    def json_item_list(cls, entities: list[Item], http_request: Request | None) -> JSONResponse:
        """Build JSON response for a list of items."""
        return JSONResponse(
            content=ItemListResponseDTO.from_entities(entities).to_dict(),
            headers=cls.item_ref_headers(body_reference=None, http_request=http_request),
        )

    @classmethod
    def json_item_stats(
        cls, stats: dict[str, Any], http_request: Request | None
    ) -> JSONResponse:
        """Build JSON response for item statistics."""
        return JSONResponse(
            content=ItemStatsResponseDTO.from_stats(stats).to_dict(),
            headers=cls.item_ref_headers(body_reference=None, http_request=http_request),
        )

    @classmethod
    def respond_item_list(
        cls, result: Result[list[Item], Any], http_request: Request | None
    ) -> JSONResponse:
        """Raise on failure, then JSON-wrap a list of items."""
        return cls.json_item_list(cls._success_payload(result), http_request)

    @classmethod
    def respond_item_stats(
        cls, result: Result[dict[str, Any], Any], http_request: Request | None
    ) -> JSONResponse:
        """Raise on failure, then JSON-wrap statistics."""
        return cls.json_item_stats(cls._success_payload(result), http_request)

    @classmethod
    def respond_item(
        cls, result: Result[Item, Any], http_request: Request | None
    ) -> JSONResponse:
        """Raise on failure, then JSON-wrap one item (no reference urn)."""
        return cls.json_item(cls._success_payload(result), http_request)

    @classmethod
    def respond_item_with_ref(
        cls,
        result: Result[Item, Any],
        http_request: Request | None,
        *,
        reference_urn: str | None,
    ) -> JSONResponse:
        """Raise on failure, then JSON-wrap one item with optional ``reference_urn`` echo."""
        return cls.json_item(
            cls._success_payload(result), http_request, reference_urn=reference_urn
        )

    @classmethod
    def respond_created_item(
        cls,
        result: Result[Item, Any],
        http_request: Request | None,
        *,
        reference_urn: str | None,
    ) -> JSONResponse:
        """Like :func:`respond_item_with_ref` but with HTTP 201 Created."""
        return cls.json_item(
            cls._success_payload(result),
            http_request,
            reference_urn=reference_urn,
            status_code=HTTPStatus.CREATED,
        )

    @classmethod
    def unwrap_item_or_404(cls, result: Result[Item | None, Any], *, item_id: str) -> Item:
        """Map service ``Result[Item | None]`` to entity or raise HTTP errors."""
        cls.raise_bad_request_if_failure(result)
        if result.value is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with ID '{item_id}' not found",
            )
        return result.value

    @classmethod
    def unwrap_deleted_or_404(cls, result: Result[bool, Any], *, item_id: str) -> None:
        """Verify deletion result or raise 404."""
        cls.raise_bad_request_if_failure(result)
        if not result.value:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with ID '{item_id}' not found",
            )

    @classmethod
    def json_delete_message(cls, item_id: str, http_request: Request | None) -> JSONResponse:
        """Build JSON response for successful deletion."""
        return JSONResponse(
            content={"message": f"Item '{item_id}' deleted successfully"},
            headers=cls.item_ref_headers(
                body_reference=None,
                http_request=http_request,
            ),
        )


__all__ = ["ItemHttpResponseBuilder"]
