import strawberry
import datetime
import typing

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

SectionGQLModel = Annotated["SectionGQLModel", strawberry.lazy(".SectionGQLModel")]
ItemGQLModel = Annotated["ItemGQLModel", strawberry.lazy(".ItemGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Type representing a part in the section"""
)
class PartGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).parts
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Part's name (part for Student)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Part's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Part's order""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="Retrieves the section owning this part")
    async def section(self, info: strawberry.types.Info) -> typing.Optional["SectionGQLModel"]:
        from .SectionGQLModel import SectionGQLModel
        result = await SectionGQLModel.resolve_reference(info, self.section_id)
        return result

    @strawberry.field(description="Retrieves the items related to this part")
    async def items(self, info: strawberry.types.Info) -> typing.List["ItemGQLModel"]:
        loader = getLoadersFromInfo(info).items
        result = await loader.filter_by(part_id=self.id)
        return result


@strawberry.input
class PartUpdateGQLModel:
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None