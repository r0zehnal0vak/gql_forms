import strawberry
import datetime
import typing

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

FormGQLModel = Annotated["FormGQLModel", strawberry.lazy(".FormGQLModel")]
RequestGQLModel = Annotated["RequestGQLModel", strawberry.lazy(".RequestGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a request history item"""
)
class HistoryGQLModel:
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).histories
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""History comment""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Request which history belongs to""")
    async def request(self, info: strawberry.types.Info) -> "RequestGQLModel":
        from .RequestGQLModel import RequestGQLModel
        result = await RequestGQLModel.resolve_reference(info, self.request_id)
        return result

    @strawberry.field(description="""History form""")
    async def form(self, info: strawberry.types.Info) -> "FormGQLModel":
        from .FormGQLModel import FormGQLModel
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result