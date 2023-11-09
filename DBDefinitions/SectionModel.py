import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey, Integer

from .uuid import UUIDFKey, UUIDColumn
from .base import BaseModel

class SectionModel(BaseModel):
    __tablename__ = "formsections"

    # requestId = Column(ForeignKey("requests.id"), primary_key=True)
    # key is st sys structure name pr as id, fk follpw by id in lower letter

    id = UUIDColumn()
    name = Column(String)

    form_id = Column(ForeignKey("forms.id"), index=True)
    order = Column(Integer)
    status = Column(String)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

