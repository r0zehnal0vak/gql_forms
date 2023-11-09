import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import String, DateTime, ForeignKey

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class ItemCategoryModel(BaseModel):
    __tablename__ = "formitemcategories"

    id = UUIDColumn()
    name = Column(String)
    name__en = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)