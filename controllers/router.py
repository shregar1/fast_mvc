"""Example API router."""

from http import HTTPStatus

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from constants.http_headers import x_reference_urn_headers
from controllers.apis.v1.example.create import ExampleCreateController
from dtos.responses.abstraction import IResponseDTO

router = APIRouter(prefix="/example", tags=["Example"])
controller = ExampleCreateController()


@router.post("", response_model=IResponseDTO, status_code=HTTPStatus.CREATED)
async def create_example(request: Request, payload: dict) -> JSONResponse:
    """Create an example via class-based controller."""
    request.state.api_name = "create_example"
    urn = getattr(request.state, "urn", "urn:req:default")
    user_urn = getattr(request.state, "user_urn", "")
    user_id = getattr(request.state, "user_id", "")

    try:
        dto = await controller.handle_create_example(
            request=request,
            urn=urn,
            user_urn=user_urn,
            payload=payload,
            headers=dict(request.headers),
            api_name="create_example",
            user_id=str(user_id),
        )
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=dto.model_dump(),
            headers=x_reference_urn_headers(getattr(dto, "reference_urn", None)),
        )
    except Exception as err:
        response_dto, http_status = controller.handle_exception(
            err,
            request,
            event_name="example.create",
            force_http_ok=False,
            fallback_message="Failed to create example.",
        )
        return JSONResponse(
            status_code=http_status, content=response_dto.model_dump(),
        )
