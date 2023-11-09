import sqlalchemy
from sqlalchemy.schema import Column
from sqlalchemy import Uuid, String, DateTime, ForeignKey

from .uuid import uuid, UUIDFKey, UUIDColumn
from .base import BaseModel

class HistoryModel(BaseModel):
    __tablename__ = "formhistories"

    id = UUIDColumn()
    name = Column(String)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    request_id = Column(ForeignKey("formrequests.id"), index=True, nullable=True)
    form_id = Column(ForeignKey("forms.id"), index=True, nullable=True)

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)

