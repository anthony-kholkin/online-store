import time
from typing import Callable, Awaitable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        address = f"{request.client.host}:{request.client.port} - " if request.client else ""

        logger.info(
            f'{address}"{request.method} {request.url.path}{request.url.query}" '
            f"{response.status_code} - Time taken: {process_time:.2f}s"
        )

        return response
