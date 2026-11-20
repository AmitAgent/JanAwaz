from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ca_number import InvalidCANumber, normalize_ca_number

router = APIRouter(prefix="/connections", tags=["connections"])


class ValidateRequest(BaseModel):
    discom: Literal["SBPDCL", "NBPDCL"]
    ca_number: str = Field(min_length=1, max_length=64)


class ValidateResponse(BaseModel):
    discom: str
    ca_number_normalized: str


@router.post("/validate", response_model=ValidateResponse)
def validate_connection(body: ValidateRequest) -> ValidateResponse:
    """Check and normalize a CA Number. Stateless: stores nothing, reveals nothing."""
    try:
        normalized = normalize_ca_number(body.discom, body.ca_number)
    except InvalidCANumber as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return ValidateResponse(discom=body.discom, ca_number_normalized=normalized)
