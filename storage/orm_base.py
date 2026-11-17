from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from storage.orm import Analysis, engine

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False)

