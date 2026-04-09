from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime, Text, func, Float, Integer, Boolean
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship — позволяет делать user.products
    portfolio_items: Mapped[list["PortfolioItem"]] = relationship(back_populates="user")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="user")
    digests: Mapped[list["Digest"]] = relationship(back_populates="user")


class PortfolioItem(TimestampMixin, Base):
    __tablename__ = "portfolio_items"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    ticker: Mapped[str] = mapped_column(String(255), unique=False)
    quantity: Mapped[int] = mapped_column(Integer, unique=False)
    purchase_price: Mapped[float] = mapped_column(Float, unique=False)

    # Relationship
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="portfolio_items")


class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    ticker: Mapped[str] = mapped_column(String(20))
    threshold: Mapped[float] = mapped_column(Float, unique=False)
    condition: Mapped[str] = mapped_column(String(255), unique=False)
    is_active: Mapped[bool] = mapped_column(Boolean, unique=False)

    # Relationship
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="alerts")


class Signal(TimestampMixin, Base):
    __tablename__ = "signals"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    ticker: Mapped[str] = mapped_column(String(255), unique=False)
    signal: Mapped[str] = mapped_column(String(255), unique=False)
    rsi: Mapped[float] = mapped_column(Float, unique=False)
    macd: Mapped[float] = mapped_column(Float, unique=False)


class Digest(TimestampMixin, Base):
    __tablename__ = "digests"
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    content: Mapped[str] = mapped_column(Text, unique=False)

    # Relationship
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="digests")
