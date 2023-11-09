import strawberry
import datetime
import typing

from typing import Annotated
from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

FormCategoryGQLModel = Annotated["FormCategoryGQLModel", strawberry.lazy(".FormCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormTypeGQLModel:
    """
    """
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: strawberry.ID):
        loader = getLoadersFromInfo(info).formtypes
        result = await loader.load(id)
        if result is not None:
            result._type_definition = cls._type_definition  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> strawberry.ID:
        return self.id

    @strawberry.field(description="""Request's name (like Vacation)""")
    def name(self) -> str:
        return self.name

    @strawberry.field(description="""Request's name (like Vacation)""")
    def name_en(self) -> str:
        return self.name_en

    @strawberry.field(description="""Request's time of last update""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberry.field(description="""Request's time of last update""")
    async def category(self, info: strawberry.types.Info) -> typing.Optional["FormCategoryGQLModel"]:
        result = await FormCategoryGQLModel.resolve_reference(info, self.category_id)
        return result
    

@strawberry.field(description="Retrieves the form type")
async def form_type_by_id(
    self, info: strawberry.types.Info, id: strawberry.ID
) -> typing.Optional[FormTypeGQLModel]:
    result = await FormTypeGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="Retrieves the form type")
async def form_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[FormTypeGQLModel]:
    loader = getLoadersFromInfo(info).formtypes
    stmt = loader.offset(skip).limit(limit)
    result = await loader.execute_select(stmt)
    return result
