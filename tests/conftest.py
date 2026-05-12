import pytest


@pytest.fixture(autouse=True)
def _reset_sse_app_status():
    # sse_starlette stores should_exit_event as a module-level singleton bound
    # to the first event loop that touches it; TestClient spins up a fresh loop
    # per request, so the second SSE test sees an event from a dead loop.
    from sse_starlette.sse import AppStatus

    AppStatus.should_exit_event = None
    yield
    AppStatus.should_exit_event = None
