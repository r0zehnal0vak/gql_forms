import strawberry
import datetime
import typing
import uuid

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

FormGQLModel = Annotated["FormGQLModel", strawberry.lazy(".FormGQLModel")]
PartGQLModel = Annotated["PartGQLModel", strawberry.lazy(".PartGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Type representing a section in the form"""
)
class SectionGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).sections
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Section's name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Section's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Section's order""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="Retrieves the parts related to this section")
    async def parts(self, info: strawberry.types.Info) -> typing.List["PartGQLModel"]:
        loader = getLoadersFromInfo(info).parts
        result = await loader.filter_by(section_id=self.id)
        return result

    @strawberry.field(description="Retrieves the form owning this section")
    async def form(self, info: strawberry.types.Info) -> typing.Optional["FormGQLModel"]:
        from .FormGQLModel import FormGQLModel
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result


@strawberry.input
class SectionInsertGQLModel:
    name: str
    id: typing.Optional[uuid.UUID] = None
    order: typing.Optional[int] = None
    valid: typing.Optional[bool] = None

@strawberry.input
class SectionUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None
    valid: typing.Optional[bool] = None