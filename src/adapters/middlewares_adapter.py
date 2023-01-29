import hashlib
import json

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from ports.cache_interface import CacheInterface


class PreventDuplicatesMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache: CacheInterface):
        super().__init__(app)
        self.cache = cache

    async def dispatch(self, request: Request, call_next):
        fingerprint = await self.generate_fingerprint(request)

        if await self.fingerprint_exists(fingerprint=fingerprint):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)

        await self.save_fingerprint(fingerprint=fingerprint)
        try:
            response = await call_next(request)
        except Exception as exc:
            await self.delete_fingerprint(fingerprint=fingerprint)
            raise exc
        finally:
            await self.delete_fingerprint(fingerprint=fingerprint)

        return response

    @staticmethod
    async def generate_fingerprint(request: Request):
        signature = request.url.path

        if request.method in ["POST", 'PUT', 'PATCH', 'DELETE']:
            body = await request.json()
            if body:
                signature = signature + json.dumps(body)

        return hashlib.md5(signature.encode("utf")).hexdigest()

    async def save_fingerprint(self, fingerprint):
        await self.cache.set(key=fingerprint, data={}, ttl=60 * 30)

    async def delete_fingerprint(self, fingerprint):
        await self.cache.delete(key=fingerprint)

    async def fingerprint_exists(self, fingerprint):
        if await self.cache.get(key=fingerprint):
            return True

        return False
