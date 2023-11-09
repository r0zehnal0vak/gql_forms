import strawberry
import datetime
import typing
from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

PartGQLModel = Annotated["PartGQLModel", strawberry.lazy(".PartGQLModel")]
ItemTypeGQLModel = Annotated["ItemTypeGQLModel", strawberry.lazy(".ItemTypeGQLModel")]

@strawberry.input
class ItemUpdateGQLModel:
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None
    value: typing.Optional[str] = None
    type_id: typing.Optional[strawberry.ID] = None

@strawberry.federation.type(
    keys=["id"], description="""Type representing an item in the form"""
)
class ItemGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).items
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Item's name (like Name)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Item's order""")
    def order(self) -> str:
        return self.order

    @strawberry.field(description="""Item's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Item's value """)
    def value(self) -> str:
        return self.value

    @strawberry.field(description="Retrieves the part owning the item")
    async def part(self, info: strawberry.types.Info) -> typing.Optional["PartGQLModel"]:
        from .PartGQLModel import PartGQLModel
        result = await PartGQLModel.resolve_reference(info, self.part_id)
        return result

    @strawberry.field(description="Retrieves the item type")
    async def type(self, info: strawberry.types.Info) -> typing.Optional["ItemTypeGQLModel"]:
        from .ItemTypeGQLModel import ItemTypeGQLModel
        result = await ItemTypeGQLModel.resolve_reference(info, self.type_id)
        return result

   
@strawberry.field(description="Retrieves the item type")
async def item_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[ItemGQLModel]:
    result = await ItemGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.input
class FormItemInsertGQLModel:
    part_id: strawberry.ID
    name: str

    id: typing.Optional[strawberry.ID] = None
    value: typing.Optional[str] = None
    order: typing.Optional[int] = None
    type_id: typing.Optional[strawberry.ID] = None
    

@strawberry.input
class FormItemUpdateGQLModel:
    lastchange: datetime.datetime
    id: strawberry.ID

    name: typing.Optional[str] = None
    value: typing.Optional[str] = None
    order: typing.Optional[int] = None
    type_id: typing.Optional[strawberry.ID] = None
    
@strawberry.type
class FormItemResultGQLModel:
    id: strawberry.ID = None
    msg: str = None

    @strawberry.field(description="""Result of item operation""")
    async def item(self, info: strawberry.types.Info) -> typing.Optional[ItemGQLModel]:
        result = await ItemGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.field(
    description="""Updates a section."""
)
async def update(self, info: strawberry.types.Info, item: ItemUpdateGQLModel) -> "FormItemResultGQLModel":
    result = FormItemResultGQLModel()
    result.id = item.id
    result.msg = "fail"
    return result    