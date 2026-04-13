"""HTTP response helpers for the sample Item API."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from abstractions.result import Result
from dtos.requests.item import CreateItemRequestDTO, UpdateItemRequestDTO
from models.item import Item


class ItemHttpResponseBuilder:
    """Build JSON responses for item routes (flat JSON bodies for sample CRUD)."""

    @staticmethod
    def raise_unprocessable_if_dto_invalid(
        body: CreateItemRequestDTO | UpdateItemRequestDTO,
    ) -> None:
        ok, errs = body.validate()
        if not ok:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=errs,
            )

    @staticmethod
    def respond_created_item(
        result: Result[Item, Any],
        http_request: Request | None,
        *,
        reference_urn: str = "",
    ) -> JSONResponse:
        del http_request  # sample API does not attach correlation headers
        if result.is_failure:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"detail": str(result.error)},
            )
        item = result.value
        payload: dict[str, Any] = item.to_dict()
        if reference_urn:
            payload["reference_urn"] = reference_urn
        return JSONResponse(status_code=HTTPStatus.CREATED, content=payload)

    @staticmethod
    def unwrap_item_or_404(
        result: Result[Item | None, Any],
        *,
        item_id: str,
    ) -> Item:
        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=str(result.error),
            )
        if result.value is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item not found: {item_id}",
            )
        return result.value

    @staticmethod
    def json_item(entity: Item, http_request: Request | None) -> JSONResponse:
        del http_request
        return JSONResponse(content=entity.to_dict())

    @staticmethod
    def respond_item_list(
        result: Result[list[Item], Any],
        http_request: Request | None,
    ) -> JSONResponse:
        del http_request
        if result.is_failure:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"detail": str(result.error)},
            )
        items = result.value
        return JSONResponse(content=[i.to_dict() for i in items])

    @staticmethod
    def respond_item_with_ref(
        result: Result[Item, Any],
        http_request: Request | None,
        *,
        reference_urn: str = "",
    ) -> JSONResponse:
        del http_request
        if result.is_failure:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"detail": str(result.error)},
            )
        item = result.value
        payload = item.to_dict()
        if reference_urn:
            payload["reference_urn"] = reference_urn
        return JSONResponse(content=payload)

    @staticmethod
    def unwrap_deleted_or_404(
        result: Result[bool, Any],
        *,
        item_id: str,
    ) -> None:
        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=str(result.error),
            )
        if not result.value:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item not found: {item_id}",
            )

    @staticmethod
    def json_delete_message(item_id: str, http_request: Request | None) -> JSONResponse:
        del http_request
        return JSONResponse(
            content={"deleted": True, "id": item_id},
        )

    @staticmethod
    def respond_item(
        result: Result[Item, Any],
        http_request: Request | None,
    ) -> JSONResponse:
        del http_request
        if result.is_failure:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"detail": str(result.error)},
            )
        return JSONResponse(content=result.value.to_dict())

    @staticmethod
    def respond_item_stats(
        result: Result[dict[str, Any], Any],
        http_request: Request | None,
    ) -> JSONResponse:
        del http_request
        if result.is_failure:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"detail": str(result.error)},
            )
        return JSONResponse(content=result.value)
