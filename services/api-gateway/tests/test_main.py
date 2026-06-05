# services/api-gateway/tests/test_main.py

# import os
# from unittest.mock import Mock
# # Import the app — this triggers the module-level code in main.py
# import sys
# from unittest.mock import AsyncMock, Mock, patch

# from fastapi.testclient import TestClient

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# from main import app


import os
import sys
from unittest.mock import AsyncMock, Mock, patch

from fastapi.testclient import TestClient

# Import the app — this triggers the module-level code in main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from main import app

# TestClient wraps the app for synchronous testing
# (even though the app is async — TestClient handles the event loop)
client = TestClient(app)


class TestHealthEndpoints:
    """Tests for operational endpoints that K8s probes will call."""

    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_shape(self):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert data["service"] == "api-gateway"
        assert "version" in data

    def test_metrics_endpoint_returns_prometheus_format(self):
        response = client.get("/metrics")
        assert response.status_code == 200
        # Prometheus format always starts with # HELP or counter names
        assert b"gateway_requests_total" in response.content or b"# HELP" in response.content


class TestReadinessEndpoint:
    """Readiness probe checks whether upstreams are reachable."""

    def test_ready_returns_503_when_user_service_down(self):
        # Patch httpx.AsyncClient to simulate user-service being unreachable
        with patch("main.httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get = AsyncMock(side_effect=Exception("connection refused"))
            mock_client_cls.return_value = mock_client

            response = client.get("/ready")
            assert response.status_code == 503

    def test_ready_returns_200_when_user_service_healthy(self):
        # Patch httpx to simulate a healthy upstream response
        with patch("main.httpx.AsyncClient") as mock_client_cls:
            mock_response = AsyncMock()
            mock_response.status_code = 200

            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client

            response = client.get("/ready")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ready"


class TestProxyRoutes:
    """Gateway proxy routes — test the routing logic, not user-service itself."""

    def test_list_users_calls_upstream(self):
        mock_users = {"users": [{"id": 1, "name": "Test User", "email": "t@t.com", "created_at": "2024-01-01"}], "total": 1}
        with patch("main.httpx.AsyncClient") as mock_client_cls:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json = Mock(return_value=mock_users)

            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.request = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client

            response = client.get("/api/users")
            assert response.status_code == 200

    def test_upstream_timeout_returns_504(self):
        import httpx as httpx_lib
        with patch("main.httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.request = AsyncMock(side_effect=httpx_lib.TimeoutException("timeout"))
            mock_client_cls.return_value = mock_client

            response = client.get("/api/users")
            assert response.status_code == 504
            assert "timed out" in response.json()["detail"]

    def test_upstream_unreachable_returns_503(self):
        import httpx as httpx_lib
        with patch("main.httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.request = AsyncMock(side_effect=httpx_lib.RequestError("unreachable"))
            mock_client_cls.return_value = mock_client

            response = client.get("/api/users")
            assert response.status_code == 503


class TestMetricsMiddleware:
    """Verify the Prometheus middleware actually increments counters."""

    def test_request_increments_counter(self):
        from main import REQUEST_COUNT
        # Get baseline count before the request
        before = REQUEST_COUNT.labels(
            method="GET", endpoint="/health", http_status="200"
        )._value.get()

        client.get("/health")

        after = REQUEST_COUNT.labels(
            method="GET", endpoint="/health", http_status="200"
        )._value.get()

        assert after > before
