import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class ItemTypeModel(BaseModel):
    __tablename__ = "formitemtypes"

    id = UUIDColumn()
    name = Column(String)
    name__en = Column(String)

    query = Column(String)
    selector = Column(String)

    category_id = Column(ForeignKey("formitemcategories.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)