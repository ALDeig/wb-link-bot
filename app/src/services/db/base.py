from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(settings.SQLITE_DSN)
session_factory = async_sessionmaker(engine, expire_on_commit=False)
