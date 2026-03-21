"""JWT bearer auth middleware (injectable hooks)."""

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmvc_middleware.jwt_bearer_auth import JWTBearerAuthMiddleware


async def _ok(_request: Request):
    return PlainTextResponse("ok")


def _json_err(urn: str, kind, _exc):
    return JSONResponse({"urn": urn, "kind": kind}, status_code=401)


def test_skips_options():
    app = Starlette(routes=[Route("/p", _ok, methods=["GET", "OPTIONS"])])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.options("/p")
    assert r.status_code == 200


def test_unprotected_path():
    app = Starlette(routes=[Route("/health", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=["/health"],
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200


def test_missing_bearer():
    app = Starlette(routes=[Route("/api/x", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {},
        load_user=lambda _c, _u: object(),
        on_authenticated=lambda _r, _d: None,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/api/x")
    assert r.status_code == 401
    assert r.json()["kind"] == "missing_bearer"


def test_success_calls_on_authenticated():
    calls = []

    def on_auth(request, data):
        calls.append((request, data))
        request.state.user_id = data["user_id"]

    app = Starlette(routes=[Route("/api/x", _ok)])
    app.add_middleware(
        JWTBearerAuthMiddleware,
        unprotected_paths=(),
        callback_paths=(),
        decode_bearer=lambda _t, _u: {"user_id": 1, "user_urn": "u"},
        load_user=lambda _c, _u: object(),
        on_authenticated=on_auth,
        build_error_response=_json_err,
    )
    client = TestClient(app)
    r = client.get("/api/x", headers={"Authorization": "Bearer x"})
    assert r.status_code == 200
    assert calls and calls[0][1]["user_id"] == 1
