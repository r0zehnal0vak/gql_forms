import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class ItemTypeModel(BaseModel):
    __tablename__ = "formitemtypes"

    id = UUIDColumn()
    name = Column(String, comment="name of category")
    name_en = Column(String, comment="english name of category")

    query = Column(String)
    selector = Column(String)

    category_id = Column(ForeignKey("formitemcategories.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")