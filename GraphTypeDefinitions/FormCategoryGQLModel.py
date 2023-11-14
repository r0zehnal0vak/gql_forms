import strawberry
import datetime
import typing
import uuid

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

@strawberry.federation.type(
    keys=["id"], description="""Entity representing a category of form types"""
)
class FormCategoryGQLModel(BaseGQLModel):
    """
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).formcategories
    
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

#############################################################
#
# Queries
#
#############################################################

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class FormCategoryWhereFilter:
    name: str
    name_en: str

form_category_by_id = createRootResolver_by_id(
    FormCategoryGQLModel, 
    description="Retrieves the form category")

# @strawberry.field(description="Retrieves the form category")
# async def form_category_by_id(
#     self, info: strawberry.types.Info, id: uuid.UUID
# ) -> typing.Union[FormCategoryGQLModel, None]:
#     result = await FormCategoryGQLModel.resolve_reference(info=info, id=id)
#     return result


# @strawberry.field(description="Retrieves the form categories")
# async def form_category_page(
#     self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
#     where: typing.Optional[FormCategoryWhereFilter] = None
# ) -> typing.List[FormCategoryGQLModel]:
#     wf = None if where is None else strawberry.asdict(where)
#     loader = getLoadersFromInfo(info).formcategories
#     result = await loader.page(skip=skip, limit=limit, where=wf)
#     return result


form_category_page = createRootResolver_by_page(
    scalarType=FormCategoryGQLModel,
    whereFilterType=FormCategoryWhereFilter,
    description='Retrieves the form categories',
    loaderLambda=lambda info: getLoadersFromInfo(info).formcategories
)
#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class FormCategoryInsertGQLModel:
    name: str = strawberry.field(description="Category name")
    
    name_en: typing.Optional[str] = None
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    valid: typing.Optional[bool] = True
    createdby: strawberry.Private[uuid.UUID] = None

@strawberry.input(description="")
class FormCategoryUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="category name", default=None)
    name_en: typing.Optional[str] = None
    valid: typing.Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="")
class FormCategoryResultGQLModel:
    id: uuid.UUID
    msg: str

    @strawberry.field(description="")
    async def category(self, info: strawberry.types.Info) -> FormCategoryGQLModel:
        return await FormCategoryGQLModel.resolve_reference(info, self.id)


@strawberry.mutation(description="")
async def form_category_insert(self, info: strawberry.types.Info, form_category: FormCategoryInsertGQLModel) -> FormCategoryResultGQLModel:
    user = getUserFromInfo(info)
    form_category.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).formcategories
    row = await loader.insert(form_category)
    result = FormCategoryResultGQLModel(id=row.id, msg="ok")
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="")
async def form_category_update(self, info: strawberry.types.Info, form_category: FormCategoryUpdateGQLModel) -> FormCategoryResultGQLModel:
    user = getUserFromInfo(info)
    form_category.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).formcategories
    row = await loader.update(form_category)
    result = FormCategoryResultGQLModel(id=form_category.id, msg="ok")
    result.msg = "fail" if row is None else "ok"
    result.id = form_category.id
    return result   