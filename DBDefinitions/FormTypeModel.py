import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey

from .uuid import uuid, UUIDFKey, UUIDColumn
from .base import BaseModel

class FormTypeModel(BaseModel):
    __tablename__ = "formtypes"

    id = UUIDColumn()
    name = Column(String)
    name_en = Column(String)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    category_id = Column(ForeignKey("formcategories.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)