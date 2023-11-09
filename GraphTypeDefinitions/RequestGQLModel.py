import strawberry
import datetime
import typing

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]
HistoryGQLModel = Annotated["HistoryGQLModel", strawberry.lazy("HistoryGQLModel")]


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
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).requests
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Request's time of last update""")
    def creator(self) -> "UserGQLModel":
        from .externals import UserGQLModel
        return UserGQLModel(id=self.createdby)

    @strawberry.field(description="""Request's time of last update""")
    async def histories(self, info: strawberry.types.Info) -> typing.List["HistoryGQLModel"]:
        loader = getLoadersFromInfo(info).histories
        result = await loader.filter_by(request_id=self.id)
        return result
    

@strawberry.field(description="""Finds an request by their id""")
async def request_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[RequestGQLModel]:
    result = await RequestGQLModel.resolve_reference(info, id)
    return result

@strawberry.field(description="Retrieves all requests")
async def requests_page(
    self, info: strawberry.types.Info, skip: int=0, limit: int=10
) -> typing.List[RequestGQLModel]:
    loader = getLoadersFromInfo(info).requests
    result = await loader.execute_select(requestselect.offset(skip).limit(limit))
    return result

@strawberry.field(description="""Finds an request by their id""")
async def requests_by_creator(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.List[RequestGQLModel]:
    loader = getLoadersFromInfo(info).requests
    result = await loader.filter_by(createdby=id)
    return result

@strawberry.field(description="Retrieves requests by three letters in their name")
async def requests_by_letters(
    self, info: strawberry.types.Info, letters: str
) -> typing.List[RequestGQLModel]:
    async with withInfo(info) as session:
        requests = await resolveRequestsByThreeLetters(session, letters=letters)
        return requests