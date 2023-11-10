import strawberry
import datetime
import typing
import uuid

from utils.Dataloaders import getLoadersFromInfo, getUserFromInfo

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormCategoryGQLModel:
    """
    """
    @classmethod
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).formcategories
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
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


#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the form category")
async def form_category_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Union[FormCategoryGQLModel, None]:
    result = await FormCategoryGQLModel.resolve_reference(info=info, id=id)
    return result

@strawberry.field(description="Retrieves the form category")
async def form_category_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10
) -> typing.List[FormCategoryGQLModel]:
    loader = getLoadersFromInfo(info).formcategories
    result = await loader.page(skip=skip, limit=limit)
    return result

#############################################################
#
# Mutations
#
#############################################################

@strawberry.input
class FormCategoryInsertGQLModel:
    name: str
    
    id: typing.Optional[uuid.UUID] = None
    valid: typing.Optional[bool] = True

@strawberry.input
class FormCategoryUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID

    name: typing.Optional[str] = None
    valid: typing.Optional[bool] = None
