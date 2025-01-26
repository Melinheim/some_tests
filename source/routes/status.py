from fastapi import APIRouter, status

from models.status import StatusSchema

router = APIRouter(prefix='/status', tags=['Status API'])


@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=StatusSchema,
)
def status_check() -> StatusSchema:
    """Status check"""
    return StatusSchema(status='serving')
