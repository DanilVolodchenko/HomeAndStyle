from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from loguru import logger

from .exceptions import HomeAndStyleBaseException

def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.error(f'Validation error: ({exc.__class__.__name__}) {exc}')
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=f'Bad request {exc}')


def internal_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f'Internal server error: ({exc.__class__.__name__}) {exc}')
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=f'Internal server error'
    )


def home_and_style_exception(request: Request, exc: HomeAndStyleBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=str(exc)
    )