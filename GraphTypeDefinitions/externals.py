import strawberry
import uuid

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return UserGQLModel(id=id)

