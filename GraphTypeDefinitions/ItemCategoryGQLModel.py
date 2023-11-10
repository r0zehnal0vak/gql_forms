import strawberry
import typing
import datetime
import uuid

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

@strawberry.federation.type(
    keys=["id"], 
    name="FormItemCategoryGQLModel",
    description="""Type representing an item category"""
)
class ItemCategoryGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).itemcategories
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
        return self.id

    @strawberry.field(description="""Category name""")
    def name(self) -> str:
        return self.name
    
#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the item categories")
async def item_category_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[ItemCategoryGQLModel]:
    loader = getLoadersFromInfo(info).itemcategories
    result = await loader.page(skip=skip, limit=limit)
    return result

@strawberry.field(description="Retrieves the item category")
async def item_category_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[ItemCategoryGQLModel]:
    result = await ItemCategoryGQLModel.resolve_reference(info=info, id=id)
    return result

#############################################################
#
# Mutations
#
#############################################################


@strawberry.input(description="")
class FormItemCategoryInsertGQLModel:
    name: str
    id: typing.Optional[uuid.UUID] = None
    


@strawberry.input(description="")
class FormItemCategoryUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID

    name: typing.Optional[str] = None
