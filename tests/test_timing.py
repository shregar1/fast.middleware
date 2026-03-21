"""Response timing middleware."""

import asyncio

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fast_middleware import DEFAULT_RESPONSE_TIME_HEADER, ResponseTimingMiddleware


async def slow(_request: Request):
    await asyncio.sleep(0.01)
    return PlainTextResponse("ok")


def test_x_response_time_header():
    app = Starlette(routes=[Route("/", slow)])
    app.add_middleware(ResponseTimingMiddleware)
    client = TestClient(app)
    r = client.get("/")
    assert DEFAULT_RESPONSE_TIME_HEADER in r.headers
    val = float(r.headers[DEFAULT_RESPONSE_TIME_HEADER])
    assert val >= 0.01


def test_x_response_time_milliseconds():
    app = Starlette(routes=[Route("/", slow)])
    app.add_middleware(ResponseTimingMiddleware, unit_seconds=False)
    client = TestClient(app)
    r = client.get("/")
    assert float(r.headers[DEFAULT_RESPONSE_TIME_HEADER]) >= 10.0
