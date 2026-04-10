"""Conexión async a Postgres para payment-service."""

# BUG: credenciales hardcodeadas. Esto es un problema de seguridad y de
# configuración: no puedes cambiarlas sin reconstruir la imagen, y dejarlas
# así en un repo público equivale a publicar tus contraseñas.
#
# Mira availability-service/app/db.py para ver cómo se construye la URL
# leyendo POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, etc. con os.getenv().
# Las variables ya están en .env.example.
import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base, Payment

_PG_USER = os.getenv("POSTGRES_USER")
_PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
_PG_DB = os.getenv("POSTGRES_DB")
_PG_HOST = os.getenv("POSTGRES_HOST")
_PG_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql+asyncpg://{_PG_USER}:{_PG_PASSWORD}@{_PG_HOST}:{_PG_PORT}/{_PG_DB}"


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
