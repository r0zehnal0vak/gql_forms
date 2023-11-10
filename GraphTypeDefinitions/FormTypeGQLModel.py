import strawberry
import datetime
import typing
import uuid

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
    async def resolve_reference(cls, info: strawberry.types.Info, id: uuid.UUID):
        loader = getLoadersFromInfo(info).formtypes
        result = await loader.load(id)
        if result is not None:
            result.__strawberry_definition__ = cls.__strawberry_definition__  # little hack :)
        return result

    @strawberry.field(description="""Entity primary key""")
    def id(self) -> uuid.UUID:
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
        from .FormCategoryGQLModel import FormCategoryGQLModel
        result = await FormCategoryGQLModel.resolve_reference(info, self.category_id)
        return result
    
#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the form type")
async def form_type_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[FormTypeGQLModel]:
    result = await FormTypeGQLModel.resolve_reference(info=info, id=id)
    return result

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class FormTypeWhereFilter:
    name: str
    name_en: str

@strawberry.field(description="Retrieves the form type")
async def form_type_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[FormTypeWhereFilter] = None
) -> typing.List[FormTypeGQLModel]:
    loader = getLoadersFromInfo(info).formtypes
    wf = None if where is None else strawberry.asdict(where)
    result = await loader.page(skip=skip, limit=limit, where=wf)
    return result

#############################################################
#
# Mutations
#
#############################################################

@strawberry.input
class FormTypeInsertGQLModel:
    name: str
    
    id: typing.Optional[uuid.UUID] = None
    valid: typing.Optional[bool] = True

@strawberry.input
class FormTypeUpdateGQLModel:
    lastchange: datetime.datetime
    id: uuid.UUID

    name: typing.Optional[str] = None
    valid: typing.Optional[bool] = None

@strawberry.type(description="")
class FormTypeResultGQLModel:
    id: uuid.UUID
    msg: str