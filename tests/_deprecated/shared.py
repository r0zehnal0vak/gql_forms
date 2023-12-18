import sqlalchemy
import sys
import asyncio
import logging
import os

# setting path
#sys.path.append("../gql_forms")

import pytest

# from ..uoishelpers.uuid import UUIDColumn
os.environ.setdefault("DEMO", "True")

from DBDefinitions import (
    BaseModel,
    FormModel,
    FormTypeModel,
    FormCategoryModel,
    PartModel,
    SectionModel,
    ItemModel,
    ItemTypeModel,
    ItemCategoryModel,
    RequestModel,
    HistoryModel
)


async def prepare_in_memory_sqllite():
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker

    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


from utils.DBFeeder import get_demodata


async def prepare_demodata(async_session_maker):
    data = get_demodata()

    from uoishelpers.feeders import ImportModels

    await ImportModels(
        async_session_maker,
        [
            FormModel,
            FormTypeModel,
            FormCategoryModel,
            PartModel,
            SectionModel,
            ItemModel,
            ItemTypeModel,
            ItemCategoryModel,
            RequestModel,
            HistoryModel
        ],
        data,
    )


from utils.Dataloaders import createLoadersContext
from utils.gql_ug_proxy import createProxy
def createContext(asyncSessionMaker, withuser=True):
    loadersContext = createLoadersContext(asyncSessionMaker)
    user = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "name": "John",
        "surname": "Newbie",
        "email": "john.newbie@world.com"
    }
    if withuser:
        loadersContext["user"] = user

    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    proxy = createProxy(GQLUG_ENDPOINT_URL)
    loadersContext["ug_connection"] = proxy.connection(authorizationToken=None)
    
    return loadersContext

def createInfo(asyncSessionMaker, withuser=True):
    class Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        
    class Info():
        @property
        def context(self):
            context = createContext(asyncSessionMaker, withuser=withuser)
            context["request"] = Request()
            return context
        
    return Info()


from GraphTypeDefinitions import schema

def CreateSchemaFunction():
    async def result(query, variables={}):

        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        print(f"query for {query} with {variables}")
        resp = await schema.execute(
            query=query, 
            variable_values=variables, 
            context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        logging.debug(f"response: {respdata}")

        result = {"data": respdata, "errors": resp.errors}
        return result

    return result