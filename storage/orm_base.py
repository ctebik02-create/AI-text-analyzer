from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from storage.orm import Analysis, engine
from sqlalchemy import select, func
from models.schemas import AIOutput
from fastapi import HTTPException

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False)

async def add_analysis_to_db(ai_analysis: AIOutput, input_text: str) -> Analysis:


    async with SessionLocal() as session:
        async with session.begin():
            analysis = Analysis(input_text=input_text, summary=ai_analysis.summary,
                                sentiment=ai_analysis.sentiment)
            session.add(analysis)

            return analysis

async def get_analyses_from_db():

    async with SessionLocal() as session:
        stmt = select(Analysis).order_by(Analysis.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_analysis_by_id_from_db(analysis_id: int):
    async with SessionLocal() as session:
        stmt = select(Analysis).where(Analysis.id == analysis_id)
        result = await session.execute(stmt)
        analysis = result.scalar_one_or_none()
        if analysis:
            return analysis
        raise HTTPException(status_code=404, detail="Analysis not found")


#for tests
async def count_analyses_for_test():
    async with SessionLocal() as session:
        stmt = select(func.count()).select_from(Analysis)
        result = await session.execute(stmt)
        return result.scalar_one()
