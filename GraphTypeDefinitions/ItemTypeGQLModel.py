import strawberry
import typing
import datetime
import uuid

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

ItemCategoryGQLModel = Annotated["ItemCategoryGQLModel", strawberry.lazy(".ItemCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], 
    name="FormItemTypeGQLModel",
    description="""Type representing an item type"""
)
class ItemTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).itemtypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""timestamp""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Type name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Type category""")
    async def category(self, info: strawberry.types.Info) -> typing.Optional["ItemCategoryGQLModel"]:
        from .ItemCategoryGQLModel import ItemCategoryGQLModel
        #result = await ItemCategoryGQLModel(info, self.category_id)
        return await ItemCategoryGQLModel.resolve_reference(info=info, id=self.category_id)
    
#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the item types")
async def item_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[ItemCategoryGQLModel]:
    loader = getLoadersFromInfo(info).itemtypes
    result = await loader.page(skip=skip, limit=limit)
    return result


@strawberry.field(description="Retrieves the item type")
async def item_type_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[ItemTypeGQLModel]:
    result = await ItemTypeGQLModel.resolve_reference(info=info, id=id)
    return result

#############################################################
#
# Mutations
#
#############################################################


@strawberry.input(description="")
class FormItemTypeInsertGQLModel:
    name: str
    id: typing.Optional[uuid.UUID] = None

@strawberry.input(description="")
class FormItemTypeUpdateGQLModel:
    id: uuid.UUID
    lastchange: datetime.datetime
    name: typing.Optional[str] = None
    order: typing.Optional[int] = None


@strawberry.type(description="")
class FormItemTypeResultGQLModel:
    id: uuid.UUID
    msg: str

    @strawberry.field(description="")
    async def item_type(self, info: strawberry.types.Info) -> "ItemTypeGQLModel":
        result = await ItemTypeGQLModel.resolve_reference(info, self.id)
        return result

@strawberry.mutation(description="")
async def form_item_type_insert(self, info: strawberry.types.Info, item_type: FormItemTypeInsertGQLModel) -> FormItemTypeResultGQLModel:
    loader = getLoadersFromInfo(info).itemtypes
    row = await loader.insert(item_type)
    result = FormItemTypeResultGQLModel(msg="fail", id=None)
    result.msg = "fail" if row is None else "ok"
    result.id = None if row is None else row.id       
    return result


@strawberry.mutation
async def form_item_type_update(self, info: strawberry.types.Info, item_type: FormItemTypeUpdateGQLModel) -> FormItemTypeResultGQLModel:
    loader = getLoadersFromInfo(info).itemtypes
    row = await loader.update(item_type)
    result = FormItemTypeResultGQLModel(msg="fail", id=None)
    result.msg = "fail" if row is None else "ok"
    result.id = item_type.id       
    return result