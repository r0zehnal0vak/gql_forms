import strawberry
import datetime
import typing
import uuid

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
HistoryGQLModel = Annotated["HistoryGQLModel", strawberry.lazy(".HistoryGQLModel")]


# define the type help to get attribute name and name
@strawberry.federation.type(
    keys=["id"], description="""Entity representing a request (digital form of a paper, aka "student request to the dean")"""
)
class RequestGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).requests
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Request's time of last update""")
    def creator(self) -> typing.Optional["UserGQLModel"]:
        from .externals import UserGQLModel
        #result = await UserGQLModel.resolve_reference(id=self.createdby)
        return UserGQLModel(id=self.createdby)

    @strawberry.field(description="""Request's time of last update""")
    async def histories(self, info: strawberry.types.Info) -> typing.List["HistoryGQLModel"]:
        loader = getLoadersFromInfo(info).histories
        result = await loader.filter_by(request_id=self.id)
        return result
    
#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="""Finds an request by their id""")
async def request_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[RequestGQLModel]:
    result = await RequestGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="Retrieves all requests")
async def requests_page(
    self, info: strawberry.types.Info, skip: int=0, limit: int=10
) -> typing.List[RequestGQLModel]:
    loader = getLoadersFromInfo(info).requests
    result = await loader.page(skip=skip, limit=limit)
    return result

@strawberry.field(description="""Finds an request by their id""")
async def requests_by_creator(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.List[RequestGQLModel]:
    loader = getLoadersFromInfo(info).requests
    result = await loader.filter_by(createdby=id)
    return result

@strawberry.field(description="Retrieves requests by three letters in their name")
async def requests_by_letters(
    self, info: strawberry.types.Info, letters: str
) -> typing.List[RequestGQLModel]:
    return []
    # async with withInfo(info) as session:
    #     requests = await resolveRequestsByThreeLetters(session, letters=letters)
    #     return requests

#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class FormRequestInsertGQLModel:
    name: str
    id: typing.Optional[uuid.UUID] = None
    


@strawberry.input(description="")
class FormRequestUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID

    name: typing.Optional[str] = None
