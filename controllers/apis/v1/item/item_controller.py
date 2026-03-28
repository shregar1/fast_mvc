"""Item Controller - Example controller implementation.

Demonstrates FastMVC controller patterns with FastAPI routes.
"""

from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from abstractions.controller import IController
from abstractions.result import Result
from constants.http_headers import X_REFERENCE_URN, x_reference_urn_headers
from dtos.requests.item import CreateItemRequestDTO, UpdateItemRequestDTO
from dtos.responses.item import (
    ItemListResponseDTO,
    ItemResponseDTO,
    ItemStatsResponseDTO,
)
from services.item.item_service import ItemService

# Create router
router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
    },
)


def _item_response_headers(
    body_reference: str | None,
    http_request: Request | None,
) -> dict[str, str]:
    """Prefer body ``reference_number``; else echo ``x-reference-urn`` from the request."""
    ref = body_reference
    if ref is None and http_request is not None:
        ref = http_request.headers.get(X_REFERENCE_URN)
    return x_reference_urn_headers(ref)


class ItemController(IController):
    """Controller for item management endpoints.

    Provides CRUD operations and business actions for items.

    Example:
        # In your main app:
        from controllers.apis.v1.item.item_controller import router
        app.include_router(router)

    """

    def __init__(self, service: ItemService | None = None) -> None:
        """Initialize controller with service.

        Args:
            service: Item service (creates new if None)

        """
        self._service = service or ItemService()

    def _handle_result(
        self, result: Result, status_code: int = HTTPStatus.OK
    ) -> JSONResponse:
        """Handle service result and convert to HTTP response.

        Args:
            result: Service operation result
            status_code: HTTP status code for success

        Returns:
            JSONResponse

        """
        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        if result.value is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Resource not found",
            )

        return JSONResponse(
            status_code=status_code,
            content=result.value.to_dict()
            if hasattr(result.value, "to_dict")
            else result.value,
        )

    # CRUD Endpoints

    async def create(
        self, body: CreateItemRequestDTO, http_request: Request | None = None
    ) -> JSONResponse:
        """Create a new item.

        Args:
            body: Create item request
            http_request: Incoming HTTP request (for ``x-reference-urn`` echo)

        Returns:
            Created item response

        """
        # Validate request
        is_valid, errors = body.validate()
        if not is_valid:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"errors": errors},
            )

        # Create item
        result = await self._service.create_item(
            name=body.name,
            description=body.description,
        )

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        # Convert to response DTO (echo client reference_number as reference_urn)
        response = ItemResponseDTO.from_entity(
            result.value, reference_urn=body.reference_number
        )

        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=response.to_dict(),
            headers=_item_response_headers(body.reference_number, http_request),
        )

    async def get_by_id(self, item_id: str, http_request: Request | None = None) -> JSONResponse:
        """Get item by ID.

        Args:
            item_id: Item identifier

        Returns:
            Item response

        """
        result = await self._service.get_item(item_id)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        if result.value is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with ID '{item_id}' not found",
            )

        response = ItemResponseDTO.from_entity(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def get_all(self, http_request: Request | None = None) -> JSONResponse:
        """Get all items.

        Returns:
            List of items

        """
        result = await self._service.get_all_items()

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemListResponseDTO.from_entities(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def update(
        self,
        item_id: str,
        body: UpdateItemRequestDTO,
        http_request: Request | None = None,
    ) -> JSONResponse:
        """Update an item.

        Args:
            item_id: Item identifier
            body: Update item request
            http_request: Incoming HTTP request (for ``x-reference-urn`` echo)

        Returns:
            Updated item response

        """
        # Validate request
        is_valid, errors = body.validate()
        if not is_valid:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"errors": errors},
            )

        # Update item
        result = await self._service.update_item(
            item_id=item_id,
            name=body.name,
            description=body.description,
        )

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemResponseDTO.from_entity(
            result.value, reference_urn=body.reference_number
        )
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(body.reference_number, http_request),
        )

    async def delete(self, item_id: str, http_request: Request | None = None) -> JSONResponse:
        """Delete an item.

        Args:
            item_id: Item identifier

        Returns:
            Deletion confirmation

        """
        result = await self._service.delete_item(item_id)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        if not result.value:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Item with ID '{item_id}' not found",
            )

        return JSONResponse(
            content={"message": f"Item '{item_id}' deleted successfully"},
            headers=_item_response_headers(None, http_request),
        )

    # Action Endpoints

    async def complete(self, item_id: str, http_request: Request | None = None) -> JSONResponse:
        """Mark item as completed.

        Args:
            item_id: Item identifier

        Returns:
            Updated item response

        """
        result = await self._service.complete_item(item_id)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemResponseDTO.from_entity(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def uncomplete(self, item_id: str, http_request: Request | None = None) -> JSONResponse:
        """Mark item as not completed.

        Args:
            item_id: Item identifier

        Returns:
            Updated item response

        """
        result = await self._service.uncomplete_item(item_id)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemResponseDTO.from_entity(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def toggle(self, item_id: str, http_request: Request | None = None) -> JSONResponse:
        """Toggle item completion status.

        Args:
            item_id: Item identifier

        Returns:
            Updated item response

        """
        result = await self._service.toggle_item(item_id)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemResponseDTO.from_entity(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    # Query Endpoints

    async def search(self, query: str = "", http_request: Request | None = None) -> JSONResponse:
        """Search items by name.

        Args:
            query: Search query string

        Returns:
            List of matching items

        """
        result = await self._service.search_items(query)

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemListResponseDTO.from_entities(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def get_completed(self, http_request: Request | None = None) -> JSONResponse:
        """Get all completed items.

        Returns:
            List of completed items

        """
        result = await self._service.get_completed_items()

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemListResponseDTO.from_entities(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def get_pending(self, http_request: Request | None = None) -> JSONResponse:
        """Get all pending items.

        Returns:
            List of pending items

        """
        result = await self._service.get_pending_items()

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemListResponseDTO.from_entities(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )

    async def get_statistics(self, http_request: Request | None = None) -> JSONResponse:
        """Get item statistics.

        Returns:
            Statistics response

        """
        result = await self._service.get_statistics()

        if result.is_failure:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=result.error,
            )

        response = ItemStatsResponseDTO.from_stats(result.value)
        return JSONResponse(
            content=response.to_dict(),
            headers=_item_response_headers(None, http_request),
        )


# Route Definitions

_controller = ItemController()


@router.post("", response_model=dict, status_code=HTTPStatus.CREATED)
async def create_item(
    http_request: Request, body: CreateItemRequestDTO
) -> JSONResponse:
    """Create a new item."""
    return await _controller.create(body, http_request)


@router.get("", response_model=dict)
async def get_all_items(http_request: Request) -> JSONResponse:
    """Get all items."""
    return await _controller.get_all(http_request)


@router.get("/search", response_model=dict)
async def search_items(http_request: Request, query: str = "") -> JSONResponse:
    """Search items by name."""
    return await _controller.search(query, http_request)


@router.get("/completed", response_model=dict)
async def get_completed_items(http_request: Request) -> JSONResponse:
    """Get all completed items."""
    return await _controller.get_completed(http_request)


@router.get("/pending", response_model=dict)
async def get_pending_items(http_request: Request) -> JSONResponse:
    """Get all pending items."""
    return await _controller.get_pending(http_request)


@router.get("/statistics", response_model=dict)
async def get_item_statistics(http_request: Request) -> JSONResponse:
    """Get item statistics."""
    return await _controller.get_statistics(http_request)


@router.get("/{item_id}", response_model=dict)
async def get_item(http_request: Request, item_id: str) -> JSONResponse:
    """Get item by ID."""
    return await _controller.get_by_id(item_id, http_request)


@router.patch("/{item_id}", response_model=dict)
async def update_item(
    http_request: Request, item_id: str, body: UpdateItemRequestDTO
) -> JSONResponse:
    """Update an item."""
    return await _controller.update(item_id, body, http_request)


@router.delete("/{item_id}", response_model=dict)
async def delete_item(http_request: Request, item_id: str) -> JSONResponse:
    """Delete an item."""
    return await _controller.delete(item_id, http_request)


@router.post("/{item_id}/complete", response_model=dict)
async def complete_item(http_request: Request, item_id: str) -> JSONResponse:
    """Mark item as completed."""
    return await _controller.complete(item_id, http_request)


@router.post("/{item_id}/uncomplete", response_model=dict)
async def uncomplete_item(http_request: Request, item_id: str) -> JSONResponse:
    """Mark item as not completed."""
    return await _controller.uncomplete(item_id, http_request)


@router.post("/{item_id}/toggle", response_model=dict)
async def toggle_item(http_request: Request, item_id: str) -> JSONResponse:
    """Toggle item completion status."""
    return await _controller.toggle(item_id, http_request)
