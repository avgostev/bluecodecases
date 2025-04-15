from typing import List, Optional
from sqlalchemy import ForeignKey, String, Date, MetaData, TIMESTAMP, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,  check_password_hash
from app.config import SQLALCHEMY_SCHEMA

ROLE_VIEWER = 0
ROLE_USER = 1
ROLE_ADMIN = 9

class Base(DeclarativeBase):
    metadata = MetaData(schema=SQLALCHEMY_SCHEMA)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), server_default=func.now())
    updated: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), server_default=func.now(), onupdate=func.now())


class User(Base, UserMixin):
    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String(), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String())
    role: Mapped[int] =  mapped_column(default = ROLE_USER)
    
    def __repr__(self):
        return '<User %r>' % (self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)

class Sex(Base):
    __tablename__ = "dic_sex"
    
    s_name: Mapped[str] = mapped_column(String(), unique=True, index=True)

    def __repr__(self) -> str:
        return f"Sex(id={self.id!r}, s_name={self.s_name!r})"

class Result(Base):
    __tablename__ = "dic_result"
    
    s_name: Mapped[str] = mapped_column(String(), unique=True, index=True)

    def __repr__(self) -> str:
        return f"Result(id={self.id!r}, s_name={self.s_name!r})"

class Place(Base):
    __tablename__ = "dic_place"
    
    s_name: Mapped[str] = mapped_column(String(), unique=True, index=True)

    def __repr__(self) -> str:
        return f"Place(id={self.id!r}, s_name={self.s_name!r})"

class Locate(Base):
    __tablename__ = "dic_locate"
    
    s_name: Mapped[str] = mapped_column(String(), unique=True, index=True)

    def __repr__(self) -> str:
        return f"Locate(id={self.id!r}, s_name={self.s_name!r})"
    
class SLRCase(Base):
    __tablename__ = "slr_case"

    d_slr: Mapped[Date] = mapped_column(Date())
    result_id: Mapped[int] = mapped_column(ForeignKey("dic_result.id"))
    result: Mapped["Result"] = relationship(single_parent=True, lazy="joined")
    sex_id: Mapped[int] = mapped_column(ForeignKey("dic_sex.id"))
    sex: Mapped["Sex"] = relationship(single_parent=True, lazy="joined")
    place_id: Mapped[int] = mapped_column(ForeignKey("dic_place.id"))
    place: Mapped["Place"] = relationship(single_parent=True, lazy="joined")
    d_bdate: Mapped[Optional[Date]] = mapped_column(Date())
    locate_id: Mapped[int] = mapped_column(ForeignKey("dic_locate.id"))
    locate: Mapped["Locate"] = relationship(single_parent=True, lazy="joined")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    user: Mapped["User"] = relationship(single_parent=True, lazy="joined")
    deleted: Mapped[bool] = mapped_column(default=False)
    
    def d_slr_to_str(self):
        return self.d_slr.strftime('%d.%m.%Y')
    
    def d_bdate_to_str(self):
        if self.d_bdate:
            return self.d_bdate.strftime('%d.%m.%Y')
        else:
            return ""

    def __repr__(self) -> str:
        return f"SLRCase(id={self.id!r})"
