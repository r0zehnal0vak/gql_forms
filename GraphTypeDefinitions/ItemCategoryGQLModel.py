import strawberry
import typing

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

@strawberry.federation.type(
    keys=["id"], description="""Type representing an item category"""
)
class ItemCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).itemcategories
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Category name""")
    def name(self) -> str:
        return self.name
    

@strawberry.field(description="Retrieves the item categories")
async def item_category_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[ItemCategoryGQLModel]:
    loader = getLoadersFromInfo(info).itemcategories
    stmt = loader.offset(skip).limit(limit)
    result = await loader.execute_select(stmt)
    return result

@strawberry.field(description="Retrieves the item category")
async def item_category_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[ItemCategoryGQLModel]:
    result = await ItemCategoryGQLModel.resolve_reference(info=info, id=id)
    return result