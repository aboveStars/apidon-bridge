from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response  
import os

SECRETAPIKEY = os.getenv("SECRETAPIKEY")

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_key = request.headers.get("APIKEY")
        print(SECRETAPIKEY)
        if api_key is None:
            return JSONResponse(status_code=401, content={"detail": "Missing API Key"})
        
        if api_key != SECRETAPIKEY:
            return JSONResponse(status_code=403, content={"detail": "Invalid API Key"})
        
        response = await call_next(request)
        return response
