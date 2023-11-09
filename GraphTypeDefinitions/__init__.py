from typing import List, Union
import typing
import strawberry
import uuid
from contextlib import asynccontextmanager


@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context["asyncSessionMaker"]
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass


# def AsyncSessionFromInfo(info):
#     print(
#         "obsolte function used AsyncSessionFromInfo, use withInfo context manager instead"
#     )
#     return info.context["session"]

def getLoaders(info):
    return info.context['all']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################


# from gql_forms.GraphResolvers import resolveRequestsByThreeLetters

from .FormGQLModel import FormGQLModel
from .FormTypeGQLModel import FormTypeGQLModel
from .FormCategoryGQLModel import FormCategoryGQLModel

from .HistoryGQLModel import HistoryGQLModel
from .RequestGQLModel import RequestGQLModel

from .ItemGQLModel import ItemGQLModel
from .ItemTypeGQLModel import ItemTypeGQLModel
from .ItemCategoryGQLModel import ItemCategoryGQLModel

from .SectionGQLModel import SectionGQLModel
from .PartGQLModel import PartGQLModel

from .externals import UserGQLModel


@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(description="""Say hello to the world""")
    async def say_hello_forms(
        self, info: strawberry.types.Info, id: strawberry.ID
    ) -> Union[str, None]:
        result = f"Hello {id}"
        return result




###########################################################################################################################
#
#
# Mutations
#
#
###########################################################################################################################

   
@strawberry.federation.type(extend=True)
class Mutation:

    from .FormGQLModel import form_insert
    form_insert = form_insert

    from .FormGQLModel import form_update
    form_update = form_update

    #from .HistoryGQLModel import 



###########################################################################################################################
#
# Schema je pouzito v main.py, vsimnete si parametru types, obsahuje vyjmenovane modely. Bez explicitniho vyjmenovani
# se ve schema objevi jen ty struktury, ktere si strawberry dokaze odvodit z Query. Protoze v teto konkretni implementaci
# nektere modely nejsou s Query propojene je potreba je explicitne vyjmenovat. Jinak ve federativnim schematu nebude
# dostupne rozsireni, ktere tento prvek federace implementuje.
#
###########################################################################################################################

schema = strawberry.federation.Schema(Query, types=(UserGQLModel,), mutation=Mutation)
