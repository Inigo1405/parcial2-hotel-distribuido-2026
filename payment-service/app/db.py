"""Conexión async a Postgres para payment-service."""

# BUG: credenciales hardcodeadas. Esto es un problema de seguridad y de
# configuración: no puedes cambiarlas sin reconstruir la imagen, y dejarlas
# así en un repo público equivale a publicar tus contraseñas.
#
# Mira availability-service/app/db.py para ver cómo se construye la URL
# leyendo POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, etc. con os.getenv().
# Las variables ya están en .env.example.
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, Integer

from .models import Base, Payment

POSTGRES_USER = os.getenv("POSTGRES_USER", "hotel_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "hotel_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hotel_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

class Base(DeclarativeBase):
    pass

class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[str] = mapped_column(String(64), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

class ProcessedEvent(Base):
    __tablename__ = "processed_events"
    event_id: Mapped[str] = mapped_column(String(64), primary_key=True)


engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
