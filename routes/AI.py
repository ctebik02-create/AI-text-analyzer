
from fastapi import APIRouter
from models.schemas import ClientInput, AIOutput, Output
from services.nvidia_service import get_ai_output
from storage.orm_base import add_analysis_to_db, get_analyses_from_db, get_analysis_by_id_from_db

router = APIRouter()


@router.post('/analysis', response_model=AIOutput)
async def add_analysis(data: ClientInput):
    text = data.text
    ai_analysis = await get_ai_output(text)
    result = await add_analysis_to_db(ai_analysis, text)

    return result

@router.get('/analyses', response_model=list[Output])
async def get_all_analyses():
    return await get_analyses_from_db()

@router.get('/analyses/{id}', response_model=Output)
async def get_analyse_by_id(id: int):
    analysis = await get_analysis_by_id_from_db(id)
    return analysis