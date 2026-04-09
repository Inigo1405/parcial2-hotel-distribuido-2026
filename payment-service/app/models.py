from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass


class Payment(Base):
  __tablename__ = "payments"

  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  booking_id: Mapped[str] = mapped_column(String(64), nullable=False)
  amount: Mapped[int] = mapped_column(Integer, nullable=False)
  status: Mapped[str] = mapped_column(String(20), nullable=False)