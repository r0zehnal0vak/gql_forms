from uuid import uuid4
from sqlalchemy import Column, Uuid
uuid = uuid4

def UUIDFKey(comment=None, nullable=True):
    return Column(Uuid, index=True, comment=comment, nullable=nullable)

def UUIDColumn():
    return Column(Uuid, primary_key=True, comment="primary key", default=uuid)