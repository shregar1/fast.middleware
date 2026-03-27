"""Client IP extraction."""

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from fastmiddleware import (
    STATE_CLIENT_IP,
    ClientIPMiddleware,
    get_client_ip,
    read_client_ip,
)


def test_get_client_ip_from_xff():
    """Execute test_get_client_ip_from_xff operation.

    Returns:
        The result of the operation.
    """

    async def ip(request: Request):
        """Execute ip operation.

        Args:
            request: The request parameter.

        Returns:
            The result of the operation.
        """
        return JSONResponse({"ip": get_client_ip(request, trusted_proxy_depth=1)})

    app = Starlette(routes=[Route("/ip", ip, methods=["GET"])])
    client = TestClient(app)
    r = client.get("/ip", headers={"X-Forwarded-For": "203.0.113.1, 10.0.0.1"})
    assert r.json()["ip"] == "203.0.113.1"


def test_get_client_ip_ignores_xff_when_depth_zero():
    """Execute test_get_client_ip_ignores_xff_when_depth_zero operation.

    Returns:
        The result of the operation.
    """

    async def ip(request: Request):
        """Execute ip operation.

        Args:
            request: The request parameter.

        Returns:
            The result of the operation.
        """
        return JSONResponse({"ip": get_client_ip(request, trusted_proxy_depth=0)})

    app = Starlette(routes=[Route("/ip", ip, methods=["GET"])])
    client = TestClient(app)
    r = client.get("/ip", headers={"X-Forwarded-For": "203.0.113.1"})
    assert r.json()["ip"] != "203.0.113.1"


def test_x_real_ip_fallback():
    """Execute test_x_real_ip_fallback operation.

    Returns:
        The result of the operation.
    """

    async def ip(request: Request):
        """Execute ip operation.

        Args:
            request: The request parameter.

        Returns:
            The result of the operation.
        """
        return JSONResponse({"ip": get_client_ip(request, use_x_real_ip=True)})

    app = Starlette(routes=[Route("/ip", ip, methods=["GET"])])
    client = TestClient(app)
    r = client.get("/ip", headers={"X-Real-IP": "198.51.100.2"})
    assert r.json()["ip"] == "198.51.100.2"


def test_client_ip_middleware_sets_state():
    """Execute test_client_ip_middleware_sets_state operation.

    Returns:
        The result of the operation.
    """

    async def ip(request: Request):
        """Execute ip operation.

        Args:
            request: The request parameter.

        Returns:
            The result of the operation.
        """
        return JSONResponse(
            {
                "ip": read_client_ip(request),
                "raw": getattr(request.state, STATE_CLIENT_IP, None),
            }
        )

    app = Starlette(routes=[Route("/ip", ip, methods=["GET"])])
    app.add_middleware(ClientIPMiddleware, trusted_proxy_depth=1)
    client = TestClient(app)
    r = client.get("/ip", headers={"X-Forwarded-For": "198.51.100.5"})
    data = r.json()
    assert data["ip"] == "198.51.100.5"
    assert data["raw"] == "198.51.100.5"
