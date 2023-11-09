import strawberry
import typing

from typing import Annotated

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

ItemCategoryGQLModel = Annotated["ItemCategoryGQLModel", strawberry.lazy(".ItemCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Type representing an item type"""
)
class ItemTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).itemtypes
        result = await loader.load(id)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Type name""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Type category""")
    async def category(self, info: strawberry.types.Info) -> typing.Optional["ItemCategoryGQLModel"]:
        from .ItemCategoryGQLModel import ItemCategoryGQLModel
        #result = await ItemCategoryGQLModel(info, self.category_id)
        return await ItemCategoryGQLModel(info, self.category_id)
    
@strawberry.field(description="Retrieves the item types")
async def item_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[ItemCategoryGQLModel]:
    loader = getLoadersFromInfo(info).itemtypes
    stmt = loader.offset(skip).limit(limit)
    result = await loader.execute_select(stmt)
    return result


@strawberry.field(description="Retrieves the item type")
async def item_type_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[ItemTypeGQLModel]:
    result = await ItemTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.input
class FormItemInsertGQLModel:
    pass

@strawberry.input
class FormItemUpdateGQLModel:
    pass

@strawberry.type
class FormItemResultGQLModel:
    pass

@strawberry.mutation
async def form_item_insert(self, info: strawberry.types.Info, item: FormItemInsertGQLModel) -> FormItemResultGQLModel:
    loader = getLoadersFromInfo(info).items
    row = await loader.insert(item)
    result = FormItemResultGQLModel()
    result.msg = "ok"
    result.id = item.id
    if row is None:
        result.msg = "fail"
        
    return result


@strawberry.mutation
async def form_item_update(self, info: strawberry.types.Info, item: FormItemUpdateGQLModel) -> FormItemResultGQLModel:
    loader = getLoadersFromInfo(info).items
    row = await loader.update(item)
    result = FormItemResultGQLModel()
    result.msg = "ok"
    result.id = item.id
    if row is None:
        result.msg = "fail"
        
    return result