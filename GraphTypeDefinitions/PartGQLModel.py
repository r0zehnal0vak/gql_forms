import strawberry
import datetime
import typing
import uuid

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

SectionGQLModel = Annotated["SectionGQLModel", strawberry.lazy(".SectionGQLModel")]
ItemGQLModel = Annotated["ItemGQLModel", strawberry.lazy(".ItemGQLModel")]

@strawberry.federation.type(
    keys=["id"], 
    name="FormPartGQLModel",
    description="""Type representing a part in the section"""
)
class PartGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).parts
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
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

#############################################################
#
# Queries
#
#############################################################
# @strawberry.field(description="")
# async def form_part_by_id(self, info: strawberry, id: strawberry.uuid) -> "PartGQLModel":
#     loader = getLoadersFromInfo(info).parts
#     result = await loader.load(id)
#     return result

#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class FormPartInsertGQLModel:
    name: str
    section_id: uuid.UUID
    id: typing.Optional[uuid.UUID] = None
    order: typing.Optional[int] = None

@strawberry.input(description="")
class FormPartUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    section_id: typing.Optional[uuid.UUID] = None
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None