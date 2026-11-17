from fastapi import APIRouter
from models.schemas import ClientInput
from services.nvidia_service import get_ai_output


router = APIRouter()


@router.post('/analyze')
async def analyze(data: ClientInput):
    text = data.text
    result = await get_ai_output(text)
    return result


