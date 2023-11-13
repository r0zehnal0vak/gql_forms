import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Boolean

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class FormModel(BaseModel):
    __tablename__ = "forms"

    id = UUIDColumn()
    name = Column(String, comment="name of category")
    name_en = Column(String, comment="english name of category")

    status = Column(String)
    valid = Column(Boolean, default=True)
    type_id = Column(ForeignKey("formtypes.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")