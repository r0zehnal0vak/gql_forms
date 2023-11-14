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
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
)

PartGQLModel = Annotated["PartGQLModel", strawberry.lazy(".PartGQLModel")]
ItemTypeGQLModel = Annotated["ItemTypeGQLModel", strawberry.lazy(".ItemTypeGQLModel")]

@strawberry.input
class ItemUpdateGQLModel:
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None
    value: typing.Optional[str] = None
    type_id: typing.Optional[uuid.UUID] = None

@strawberry.federation.type(
    keys=["id"], 
    name="FormItemGQLModel",
    description="""Type representing an item in the form"""
)
class ItemGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).items
    
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
    rbacobject = resolve_rbacobject

    @strawberry.field(description="""Item's order""")
    def order(self) -> int:
        return self.order if self.order else 0

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
        result = None if self.type_id is None else await ItemTypeGQLModel.resolve_reference(info=info, id=self.type_id)
        return result

#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the item type")
async def item_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[ItemGQLModel]:
    result = await ItemGQLModel.resolve_reference(info=info, id=id)
    return result

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class FormItemWhereFilter:
    name: str
    name_en: str
    type_id: uuid.UUID
    value: str

@strawberry.field(description="Retrieves the item type")
async def item_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 0,
    where: typing.Optional[FormItemWhereFilter] = None
) -> typing.List[ItemGQLModel]:
    loader = getLoadersFromInfo(info).items
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip, limit, where = wf)
    return result
#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class FormItemInsertGQLModel:
    name: str = strawberry.field(description="Item name")
    part_id: uuid.UUID = strawberry.field(description="id of parent entity")

    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    value: typing.Optional[str] = None
    order: typing.Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    type_id: typing.Optional[uuid.UUID] = None
    createdby: strawberry.Private[uuid.UUID] = None 
    

@strawberry.input(description="")
class FormItemUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="Item name", default=None)
    value: typing.Optional[str] = None
    order: typing.Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    type_id: typing.Optional[uuid.UUID] = None
    changedby: strawberry.Private[uuid.UUID] = None
    
@strawberry.type
class FormItemResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of item operation""")
    async def item(self, info: strawberry.types.Info) -> typing.Optional[ItemGQLModel]:
        result = await ItemGQLModel.resolve_reference(info, self.id)
        return result
    

@strawberry.field(
    description="""Updates a section."""
)
async def item_update(self, info: strawberry.types.Info, item: FormItemUpdateGQLModel) -> "FormItemResultGQLModel":
    user = getUserFromInfo(info)
    item.changedby = uuid.UUID(user["id"])
    result = FormItemResultGQLModel()
    result.id = item.id

    loader = getLoadersFromInfo(info).items
    row = await loader.update(item)
    result.msg = "fail" if row is None else "ok"
    return result    


@strawberry.field(
    description="""Updates a section."""
)
async def item_insert(self, info: strawberry.types.Info, item: FormItemInsertGQLModel) -> "FormItemResultGQLModel":
    user = getUserFromInfo(info)
    item.createdby = uuid.UUID(user["id"])
    result = FormItemResultGQLModel()

    loader = getLoadersFromInfo(info).items
    row = await loader.insert(item)
    result.msg = "fail" if row is None else "ok"
    result.id = None if row is None else row.id
    return result    