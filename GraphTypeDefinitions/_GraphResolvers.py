import strawberry
import uuid
import datetime
import typing

UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".externals")]

@strawberry.field(description="""Entity primary key""")
def resolve_id(self) -> uuid.UUID:
    return self.id

@strawberry.field(description="""Name """)
def resolve_name(self) -> str:
    return self.name

@strawberry.field(description="""Time of last update""")
def resolve_lastchange(self) -> datetime.datetime:
    return self.lastchange

@strawberry.field(description="""Time of entity introduction""")
def resolve_created(self) -> typing.Optional[datetime.datetime]:
    return self.lastchange

@strawberry.field(description="""Who created entity""")
async def resolve_createdby(self) -> typing.Optional["UserGQLModel"]:
    from .externals import UserGQLModel
    result = None if self.createdby is None else await UserGQLModel.resolve_reference(self.createdby)
    return result

@strawberry.field(description="""Who made last change""")
async def resolve_changedby(self) -> typing.Optional["UserGQLModel"]:
    from .externals import UserGQLModel
    result = None if self.changedby is None else await UserGQLModel.resolve_reference(self.changedby)
    return result

@strawberry.field(description="""English name""")
def resolve_name_en(self) -> str:
    return self.name_en

def createAttributeScalarResolver(
    scalarType: None = None, 
    foreignKeyName: str = None,
    description="Retrieves item by its id",
    permission_classes=()
    ):

    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description, permission_classes=permission_classes)
    async def foreignkeyScalar(
        self, info: strawberry.types.Info
    ) -> typing.Optional[scalarType]:
        # 👇 self must have an attribute, otherwise it is fail of definition
        assert hasattr(self, foreignKeyName)
        id = getattr(self, foreignKeyName, None)
        
        result = None if id is None else await scalarType.resolve_reference(info=info, id=id)
        return result
    return foreignkeyScalar

def createAttributeVectorResolver(
    scalarType: None = None, 
    whereFilterType: None = None,
    foreignKeyName: str = None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10):

    assert scalarType is not None
    assert foreignKeyName is not None

    @strawberry.field(description=description)
    async def foreignkeyVector(
        self, info: strawberry.types.Info,
        skip: int = skip,
        limit: int = limit,
        where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        
        params = {foreignKeyName: self.id}
        loader = loaderLambda(info)
        assert loader is not None
        
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf, extendedfilter=params)
        return result
    return foreignkeyVector

def createRootResolver_by_id(scalarType: None, description="Retrieves item by its id"):
    assert scalarType is not None
    @strawberry.field(description=description)
    async def by_id(
        self, info: strawberry.types.Info, id: uuid.UUID
    ) -> typing.Optional[scalarType]:
        result = await scalarType.resolve_reference(info=info, id=id)
        return result
    return by_id

def createRootResolver_by_page(
    scalarType: None, 
    whereFilterType: None,
    loaderLambda = lambda info: None, 
    description="Retrieves items paged", 
    skip: int=0, 
    limit: int=10):

    assert scalarType is not None
    assert whereFilterType is not None
    
    @strawberry.field(description=description)
    async def paged(
        self, info: strawberry.types.Info, 
        skip: int=skip, limit: int=limit, where: typing.Optional[whereFilterType] = None
    ) -> typing.List[scalarType]:
        loader = loaderLambda(info)
        assert loader is not None
        wf = None if where is None else strawberry.asdict(where)
        result = await loader.page(skip=skip, limit=limit, where=wf)
        return result
    return paged
