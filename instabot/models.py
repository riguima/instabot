from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from instabot.database import db


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = 'accounts'
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[str]


Base.metadata.create_all(db)
