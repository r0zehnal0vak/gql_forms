import strawberry
import datetime
import typing

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormCategoryGQLModel:
    """
    """
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).formcategories
        result = await loader.load(id)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Name """)
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Name """)
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange


@strawberry.field(description="Retrieves the form category")
async def form_category_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Union[FormCategoryGQLModel, None]:
    result = await FormCategoryGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="Retrieves the form category")
async def form_category_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[FormCategoryGQLModel]:
    loader = getLoadersFromInfo(info).formcategories
    stmt = loader.offset(skip).limit(limit)
    result = await loader.execute_select(stmt)
    return result
