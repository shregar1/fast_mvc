"""
Service to refresh access token using a valid refresh token.
"""

from http import HTTPStatus

from constants.api_status import APIStatus
from dtos.responses.base import BaseResponseDTO
from fastmvc_errors.bad_input_error import BadInputError
from jwt import PyJWTError
from services.user.abstraction import IUserService
from fastmvc_utilities.jwt import JWTUtility


class UserRefreshService(IUserService):
    """Service to validate refresh token and issue new access and refresh tokens."""

    def __init__(
        self,
        urn: str = None,
        user_urn: str = None,
        api_name: str = None,
        user_id: str = None,
        jwt_utility: JWTUtility = None,
    ) -> None:
        super().__init__(urn, user_urn, api_name)
        self._urn = urn
        self._user_urn = user_urn
        self._api_name = api_name
        self._user_id = user_id
        self._jwt_utility = jwt_utility

    @property
    def jwt_utility(self) -> JWTUtility:
        return self._jwt_utility

    @jwt_utility.setter
    def jwt_utility(self, value: JWTUtility) -> None:
        self._jwt_utility = value

    async def run(self, refresh_token: str) -> BaseResponseDTO:
        """
        Decode refresh token and issue new access and refresh tokens.

        Args:
            refresh_token: JWT refresh token string.

        Returns:
            BaseResponseDTO with new token and refresh_token in data.

        Raises:
            BadInputError: If token is missing, invalid, or not a refresh type.
        """
        if not refresh_token or not refresh_token.strip():
            raise BadInputError(
                responseMessage="Refresh token is required.",
                responseKey="error_refresh_token_required",
                httpStatusCode=HTTPStatus.BAD_REQUEST,
            )

        try:
            payload = self.jwt_utility.decode_token(token=refresh_token.strip())
        except PyJWTError as err:
            raise BadInputError(
                responseMessage="Invalid or expired refresh token.",
                responseKey="error_refresh_token_invalid",
                httpStatusCode=HTTPStatus.UNAUTHORIZED,
            ) from err

        if payload.get("type") != "refresh":
            raise BadInputError(
                responseMessage="Invalid refresh token.",
                responseKey="error_refresh_token_invalid",
                httpStatusCode=HTTPStatus.UNAUTHORIZED,
            )

        # Build payload for new tokens (exclude type and exp)
        data = {
            k: v for k, v in payload.items()
            if k not in ("type", "exp", "iat")
        }
        if not data.get("user_id"):
            raise BadInputError(
                responseMessage="Invalid refresh token payload.",
                responseKey="error_refresh_token_invalid",
                httpStatusCode=HTTPStatus.UNAUTHORIZED,
            )

        access_token = self.jwt_utility.create_access_token(data=data)
        new_refresh_token = self.jwt_utility.create_refresh_token(data=data)

        return BaseResponseDTO(
            transactionUrn=self.urn,
            status=APIStatus.SUCCESS,
            responseMessage="Tokens refreshed successfully.",
            responseKey="success_refresh",
            data={
                "token": access_token,
                "refresh_token": new_refresh_token,
            },
        )
