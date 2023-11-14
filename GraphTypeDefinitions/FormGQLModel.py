import strawberry
import typing
import datetime
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
    resolve_rbacobject,
    createRootResolver_by_id,
    createRootResolver_by_page,
    createAttributeScalarResolver,
    createAttributeVectorResolver
)

SectionGQLModel = Annotated["SectionGQLModel", strawberry.lazy(".SectionGQLModel")]
FormTypeGQLModel = Annotated["FormTypeGQLModel", strawberry.lazy(".FormTypeGQLModel")]
UserGQLModel = Annotated["UserGQLModel", strawberry.lazy(".externals")]


@strawberry.federation.type(
    keys=["id"], description="""Entity representing a form, form is digitalized A4 sheet"""
)
class FormGQLModel(BaseGQLModel):
    """
    Type representing a request in the system.
    This class extends the base `RequestModel` from the database and adds additional fields and methods needed for use in GraphQL.
    """
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).forms
    
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

    @strawberry.field(description="""Request's validity""")
    def valid(self) -> bool:
        return self.valid

    @strawberry.field(description="""Request's status""")
    def status(self) -> typing.Optional[bool]:
        return self.status

    @strawberry.field(description="Retrieves the sections related to this form (form has several sections)")
    async def sections(
        self, info: strawberry.types.Info
    ) -> typing.List["SectionGQLModel"]:
        loader = getLoadersFromInfo(info).sections
        sections = await loader.filter_by(form_id=self.id)
        return sections

    @strawberry.field(description="Retrieves the user who has initiated this request")
    async def creator(self, info: strawberry.types.Info) -> typing.Optional["UserGQLModel"]:
        #user = UserGQLModel(id=self.createdby)
        from .externals import UserGQLModel
        result = (None 
            if self.createdby is None else 
            await UserGQLModel.resolve_reference(id=self.createdby)
        )
        return result

    @strawberry.field(description="Retrieves the type of form")
    async def type(self, info: strawberry.types.Info) -> typing.Optional["FormTypeGQLModel"]:
        from .FormTypeGQLModel import FormTypeGQLModel
        result = await FormTypeGQLModel.resolve_reference(info, id=self.type_id)
        return result
  
#############################################################
#
# Queries
#
#############################################################

@strawberry.field(description="Retrieves the form type")
async def form_by_id(
    self, info: strawberry.types.Info, id: uuid.UUID
) -> typing.Optional[FormGQLModel]:
    result = await FormGQLModel.resolve_reference(info=info, id=id)
    return result

from dataclasses import dataclass
from .utils import createInputs

@createInputs
@dataclass
class FormWhereFilter:
    name: str
    name_en: str
    valid: bool
    type_id: uuid.UUID
    createdby: uuid.UUID

@strawberry.field(description="Retrieves the form type")
async def form_page(
    self, info: strawberry.types.Info, skip: int = 0, limit: int = 10,
    where: typing.Optional[FormWhereFilter] = None
) -> typing.List[FormGQLModel]:
    wf = None if where is None else strawberry.asdict(where)
    loader = getLoadersFromInfo(info).forms
    result = await loader.page(skip, limit, where=wf)
    return result    



#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class FormInsertGQLModel:
    name: str = strawberry.field(description="form name")
    
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    form_type_id: typing.Optional[uuid.UUID] = None
    place: typing.Optional[str] = ""
    published_date: typing.Optional[datetime.datetime] = datetime.datetime.now()
    reference: typing.Optional[str] = ""
    valid: typing.Optional[bool] = True
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="")
class FormUpdateGQLModel:
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")

    name: typing.Optional[str] = strawberry.field(description="form name", default=None)
    form_type_id: typing.Optional[uuid.UUID] = None
    place: typing.Optional[str] = None
    published_date: typing.Optional[datetime.datetime] = None
    reference: typing.Optional[str] = None
    valid: typing.Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None
    
    
@strawberry.type(description="")
class FormResultGQLModel:
    id: uuid.UUID = None
    msg: str = None

    @strawberry.field(description="""Result of form operation""")
    async def form(self, info: strawberry.types.Info) -> typing.Optional[FormGQLModel]:
        result = await FormGQLModel.resolve_reference(info, self.id)
        return result
   

@strawberry.mutation
async def form_insert(self, info: strawberry.types.Info, form: FormInsertGQLModel) -> FormResultGQLModel:
    user = getUserFromInfo(info)
    form.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).forms
    row = await loader.insert(form)
    result = FormResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation
async def form_update(self, info: strawberry.types.Info, form: FormUpdateGQLModel) -> FormResultGQLModel:
    user = getUserFromInfo(info)
    form.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).forms
    row = await loader.update(form)
    result = FormResultGQLModel()
    result.msg = "fail" if row is None else "ok"
    result.id = form.id
        
    return result   