from config import DATABASE_URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import JSON, Computed, ForeignKey, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Stats(Base):
    __tablename__ = 'bot_stat'
    
    today: Mapped[date] = mapped_column(Date, primary_key=True)
    online_today: Mapped[int] = mapped_column(nullable=True)
    count_all_users: Mapped[int] = mapped_column(nullable=True)
    count_users_in_groups: Mapped[dict] = mapped_column(JSON, nullable=True)
    
class User_access(Base):
    __tablename__ = 'users_access'

    id: Mapped[int] = mapped_column(ForeignKey("users_info.id"), primary_key=True)
    subscription_activate: Mapped[bool]
    start_subscription: Mapped[date] = mapped_column(nullable=True)
    end_subscration: Mapped[date] = mapped_column(nullable=True)
    
class User(Base):
    __tablename__ = 'users_info'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    user_name: Mapped[str] = mapped_column(nullable=True)
    collage: Mapped[str] = mapped_column(nullable=True)
    group: Mapped[int] = mapped_column(nullable=True)
    subgroup: Mapped[int] = mapped_column(nullable=True)
    date_of_registration: Mapped[date]
    fast_access: Mapped[dict] = mapped_column(JSON, default=False, nullable=True)
    
class Lesson(Base):
    __tablename__ = 'lessons_on_groups'

    day: Mapped[date] = mapped_column(Date, primary_key=True)
    lessons: Mapped[dict] = mapped_column(JSON, nullable=True)
    
