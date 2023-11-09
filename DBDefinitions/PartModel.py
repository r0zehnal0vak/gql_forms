import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Integer

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class PartModel(BaseModel):
    __tablename__ = "formparts"

    id = UUIDColumn()
    name = Column(String)
    order = Column(Integer)

    section_id = Column(ForeignKey("formsections.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

