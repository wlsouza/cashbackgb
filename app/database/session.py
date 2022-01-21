from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DB_URI, echo=True)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,  # I'm setting it because T want to user 2.0 style
    class_=AsyncSession,  # To make a async session
)
