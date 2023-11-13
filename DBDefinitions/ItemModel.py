import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Integer

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class ItemModel(BaseModel):
    __tablename__ = "formitems"

    id = UUIDColumn()
    name = Column(String, comment="name of category")
    name_en = Column(String, comment="english name of category")
    
    order = Column(Integer, comment="order in parent entity")
    value = Column(String, comment="item value, with name it is named value")

    part_id = Column(ForeignKey("formparts.id"), index=True)
    type_id = Column(ForeignKey("formitemtypes.id"), index=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="when this entity has been created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="timestamp / token")
    createdby = UUIDFKey(nullable=True, comment="who's created the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True, comment="who's changed the entity")#Column(ForeignKey("users.id"), index=True, nullable=True)

    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")