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

FormGQLModel = Annotated["FormGQLModel", strawberry.lazy(".FormGQLModel")]
PartGQLModel = Annotated["PartGQLModel", strawberry.lazy(".PartGQLModel")]

@strawberry.federation.type(
    keys=["id"], 
    name="FormSectionGQLModel",
    description="""Type representing a section in the form"""
)
class SectionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info):
        return getLoadersFromInfo(info).sections
    
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

    @strawberry.field(description="""Section's order""")
    def order(self) -> int:
        return self.order

    @strawberry.field(description="Retrieves the parts related to this section")
    async def parts(self, info: strawberry.types.Info) -> typing.List["PartGQLModel"]:
        loader = getLoadersFromInfo(info).parts
        result = await loader.filter_by(section_id=self.id)
        return result

    @strawberry.field(description="Retrieves the form owning this section")
    async def form(self, info: strawberry.types.Info) -> typing.Optional["FormGQLModel"]:
        from .FormGQLModel import FormGQLModel
        result = await FormGQLModel.resolve_reference(info, self.form_id)
        return result

#############################################################
#
# Queries
#
#############################################################


#############################################################
#
# Mutations
#
#############################################################

@strawberry.input(description="")
class SectionInsertGQLModel:
    name: str = strawberry.field(description="Section name")
    form_id: uuid.UUID = strawberry.field(description="id of parent entity")
    id: typing.Optional[uuid.UUID] = strawberry.field(description="primary key (UUID), could be client generated", default=None)
    order: typing.Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    valid: typing.Optional[bool] = None
    createdby: strawberry.Private[uuid.UUID] = None 

@strawberry.input(description="")
class SectionUpdateGQLModel:
    id: uuid.UUID = strawberry.field(description="primary key (UUID), identifies object of operation")
    lastchange: datetime.datetime = strawberry.field(description="timestamp of last change = TOKEN")
    name: typing.Optional[str] = strawberry.field(description="Section name", default=None)
    order: typing.Optional[int] = strawberry.field(description="Position in parent entity", default=None)
    valid: typing.Optional[bool] = None
    changedby: strawberry.Private[uuid.UUID] = None

@strawberry.type(description="")
class SectionResultGQLModel:
    id: uuid.UUID
    msg: str

    @strawberry.field(description="")
    async def section(self, info: strawberry.types.Info) -> SectionGQLModel:
        return await SectionGQLModel.resolve_reference(info, self.id)

@strawberry.mutation(description="")
async def section_insert(self, info: strawberry.types.Info, section: SectionInsertGQLModel) -> SectionResultGQLModel:
    user = getUserFromInfo(info)
    section.createdby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.insert(section)
    result = SectionResultGQLModel()
    result.msg = "ok"
    result.id = row.id
    return result

@strawberry.mutation(description="")
async def section_update(self, info: strawberry.types.Info, section: SectionUpdateGQLModel) -> SectionResultGQLModel:
    user = getUserFromInfo(info)
    section.changedby = uuid.UUID(user["id"])
    loader = getLoadersFromInfo(info).requests
    row = await loader.update(section)
    result = SectionResultGQLModel()
    result.msg = "fail" if row is None else "ok"
    result.id = section.id
    return result   