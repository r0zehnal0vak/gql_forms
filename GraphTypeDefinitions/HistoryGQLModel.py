import strawberry
import datetime
import typing
import uuid

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo
from .BaseGQLModel import BaseGQLModel

from GraphTypeDefinitions._GraphResolvers import (
    resolve_id,
    resolve_name,
    resolve_name_en,
    resolve_changedby,
    resolve_created,
    resolve_lastchange,
    resolve_createdby,
    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
)

FormGQLModel = Annotated["FormGQLModel", strawberry.lazy(".FormGQLModel")]
RequestGQLModel = Annotated["RequestGQLModel", strawberry.lazy(".RequestGQLModel")]

@strawberry.federation.type(
    keys=["id"], 
    name="RequestHistoryGQLModel",
    description="""Entity representing a request history item"""
)
class HistoryGQLModel(BaseGQLModel):
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).histories
    
    # @classmethod
    # async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
    # implementation is inherited

    id = resolve_id
    name = resolve_name
    changedby = resolve_changedby
    lastchange = resolve_lastchange
    created = resolve_created
    createdby = resolve_createdby
    name_en = resolve_name_en

    @strawberry.field(description="""Request which history belongs to""")
    async def request(self, info: strawberry.types.Info) -> typing.Optional["RequestGQLModel"]:
        from .RequestGQLModel import RequestGQLModel
        result = await RequestGQLModel.resolve_reference(info, self.request_id)
        return result

    @strawberry.field(description="""History form""")
    async def form(self, info: strawberry.types.Info) -> typing.Optional["FormGQLModel"]:
        from .FormGQLModel import FormGQLModel
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result
    

#############################################################
#
# Queries
#
#############################################################

#############################################################
#
# Mutations
#
#############################################################


@strawberry.input(description="")
class HistoryInsertGQLModel:
    name: str = strawberry.field(description="history name")
    request_id: uuid.UUID = strawberry.field(description="id of request")
    form_id: uuid.UUID = strawberry.field(description="id of form")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    createdby: strawberry.Private[uuid.UUID] = None    

@strawberry.input(description="")
class HistoryUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="history name", default=None)
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="")
class HistoryResultGQLModel:
    id: uuid.UUID
    msg: str

    @strawberry.field(description="")
    async def history(self, info: strawberry.types.Info) -> HistoryGQLModel:
        result = await HistoryGQLModel.resolve_reference(info=info, id=self.id)
        return result

@strawberry.mutation(description="")
async def history_insert(self, info: strawberry.types.Info, history: HistoryInsertGQLModel) -> HistoryResultGQLModel:
    user = getUserFromInfo(info)
    history.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.insert(history)
    result = HistoryResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="")
async def history_update(self, info: strawberry.types.Info, history: HistoryUpdateGQLModel) -> HistoryResultGQLModel:
    user = getUserFromInfo(info)
    history.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.update(history)
    result = HistoryResultGQLModel()
    result.msg = "fail" if row is None else "ok"
    result.id = history.id
    return result   