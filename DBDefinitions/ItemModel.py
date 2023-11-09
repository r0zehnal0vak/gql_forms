import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Integer

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class ItemModel(BaseModel):
    __tablename__ = "formitems"

    id = UUIDColumn()
    name = Column(String)
    order = Column(Integer)
    value = Column(String)

    part_id = Column(ForeignKey("formparts.id"), index=True)
    type_id = Column(ForeignKey("formitemtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
