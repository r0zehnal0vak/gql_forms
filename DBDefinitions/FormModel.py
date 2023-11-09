import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Boolean

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class FormModel(BaseModel):
    __tablename__ = "forms"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    status = Column(String)
    valid = Column(Boolean, default=True)
    type_id = Column(ForeignKey("formtypes.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)