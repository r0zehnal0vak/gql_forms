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
    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
)

FormCategoryGQLModel = Annotated["FormCategoryGQLModel", strawberry.lazy(".FormCategoryGQLModel")]

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormTypeGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).formtypes
    
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

@strawberry.input(description="")
class FormTypeInsertGQLModel:
    name: str = strawberry.field(description="form type name")
    
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    valid: typing.Optional[bool] = True
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="")
class FormTypeUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="form type name", default=None)
    valid: typing.Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="")
class FormTypeResultGQLModel:
    id: uuid.UUID
    msg: str

    @strawberry.field(description="")
    async def form_type(self, info: strawberry.types.Info) -> FormTypeGQLModel:
        result = await FormTypeGQLModel.resolve_reference(info=info, id=self.id)
        return result

@strawberry.mutation(description="")
async def form_type_insert(self, info: strawberry.types.Info, form_type: FormTypeInsertGQLModel) -> FormTypeResultGQLModel:
    user = getUserFromInfo(info)
    form_type.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.insert(form_type)
    result = FormTypeResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="")
async def form_type_update(self, info: strawberry.types.Info, form_type: FormTypeUpdateGQLModel) -> FormTypeResultGQLModel:
    user = getUserFromInfo(info)
    form_type.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.update(form_type)
    result = FormTypeResultGQLModel()
    result.msg = "fail" if row is None else "ok"
    result.id = form_type.id
    return result   