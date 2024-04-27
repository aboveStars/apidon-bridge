from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response  
import os

SECRET_API_KEY = os.getenv("SECRET_API_KEY")

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_key = request.headers.get("API_KEY")
        if api_key is None:
            return JSONResponse(status_code=401, content={"detail": "Missing API Key"})
        
        if api_key != SECRET_API_KEY:
            return JSONResponse(status_code=403, content={"detail": "Invalid API Key"})
        
        response = await call_next(request)
        return response
