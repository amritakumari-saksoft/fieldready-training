"""Health endpoints."""

from fastapi import APIRouter, Response

from app.services import readiness

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Check whether the application is alive."""
    return {"status": "ok"}


@router.get("/health/ready")
def ready(response: Response) -> dict[str, str]:
    """Check whether required dependencies are available."""

    problems = readiness.check_dependencies()

    if problems:
        response.status_code = 503
        return {
            "status": "not ready",
            "problems": ", ".join(problems),
        }

    return {"status": "ready"}
