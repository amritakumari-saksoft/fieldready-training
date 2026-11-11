"""Ask endpoint."""

from fastapi import APIRouter

from app.models.schemas import AskRequest, AskResponse
from app.services import answering

router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(body: AskRequest) -> AskResponse:
    """Answer a question using retrieved sources."""

    result = answering.answer_question(body.question)

    return AskResponse(
        answer=result["answer"],
        citations=result["citations"],
    )
