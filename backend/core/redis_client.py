"""
DrugAI — Redis async client with connection pool.
"""
from __future__ import annotations

from typing import AsyncGenerator

import redis.asyncio as aioredis

from core.config import settings

_pool: aioredis.ConnectionPool | None = None
_client: aioredis.Redis | None = None


def get_pool() -> aioredis.ConnectionPool:
    global _pool
    if _pool is None:
        _pool = aioredis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=50,
            decode_responses=True,
        )
    return _pool


def get_redis() -> aioredis.Redis:
    global _client
    if _client is None:
        _client = aioredis.Redis(connection_pool=get_pool())
    return _client


async def close_redis() -> None:
    global _client, _pool
    if _client:
        await _client.close()
        _client = None
    if _pool:
        await _pool.disconnect()
        _pool = None


# ── FastAPI Dependency ─────────────────────────────────────────────────────────

async def get_redis_dep() -> AsyncGenerator[aioredis.Redis, None]:
    client = get_redis()
    try:
        yield client
    finally:
        pass  # keep connection alive; pool manages lifecycle


# ── Helpers ────────────────────────────────────────────────────────────────────

async def cache_set(key: str, value: str, expire_seconds: int = 300) -> None:
    try:
        await get_redis().set(key, value, ex=expire_seconds)
    except Exception:
        pass  # Redis unavailable — skip caching silently


async def cache_get(key: str) -> str | None:
    try:
        return await get_redis().get(key)
    except Exception:
        return None  # Redis unavailable — treat as cache miss


async def cache_delete(key: str) -> None:
    try:
        await get_redis().delete(key)
    except Exception:
        pass


async def blacklist_token(jti: str, expire_seconds: int = 3600) -> None:
    """Add a JWT token ID to the blacklist (for logout)."""
    await cache_set(f"blacklist:{jti}", "1", expire_seconds)


async def is_token_blacklisted(jti: str) -> bool:
    val = await cache_get(f"blacklist:{jti}")
    return val is not None


# ── Cache Decorator ────────────────────────────────────────────────────────────

import json
from functools import wraps
from fastapi import Request, Response
from typing import Callable, Any

def with_cache(expire_seconds: int = 300):
    """
    Cache decorator for FastAPI endpoints.
    Expects `request: Request` to be present in the endpoint signature.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request | None = kwargs.get("request")
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
                    
            if not request:
                # Fallback if no request found in kwargs/args
                return await func(*args, **kwargs)
                
            cache_key = f"cache:{request.method}:{request.url.path}:{request.url.query}"
            
            cached_data = await cache_get(cache_key)
            if cached_data:
                try:
                    return json.loads(cached_data)
                except json.JSONDecodeError:
                    pass
                    
            result = await func(*args, **kwargs)
            
            # Simple serialization - assuming result is dict or pydantic model
            if hasattr(result, "model_dump"):
                data_to_cache = result.model_dump()
            elif isinstance(result, dict) or isinstance(result, list):
                data_to_cache = result
            else:
                # Skip caching for complex objects
                return result
                
            await cache_set(cache_key, json.dumps(data_to_cache), expire_seconds)
            return result
            
        return wrapper
    return decorator
