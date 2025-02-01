from fastapi import APIRouter, status

from app.database._engine import check_availability
from app.models.status import StatusSchema

router = APIRouter(prefix='/status', tags=['Status API'])


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=StatusSchema,
)
def status_check() -> StatusSchema:
    """Status check"""
    return StatusSchema(database=check_availability())
