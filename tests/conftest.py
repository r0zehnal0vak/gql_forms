import os
import re
import json
import pytest
import logging
import fastapi
import uvicorn
from pydantic import BaseModel
from uuid import uuid1 as uuid
import random
import pytest_asyncio

def uuid1():
    return f"{uuid()}"


@pytest.fixture
def DBModels():
    from DBDefinitions import (
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
    return  [
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
        ]

from utils.DBFeeder import get_demodata
@pytest.fixture
def DemoData():
    return get_demodata()


@pytest_asyncio.fixture
async def Async_Session_Maker(DBModels):
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import sessionmaker
    from DBDefinitions import BaseModel
    asyncEngine = create_async_engine("sqlite+aiosqlite:///:memory:")
    # asyncEngine = create_async_engine("sqlite+aiosqlite:///data.sqlite")
    async with asyncEngine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_session_maker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


@pytest_asyncio.fixture
async def SQLite(Async_Session_Maker, DemoData, DBModels):
    
    from uoishelpers.feeders import ImportModels

    await ImportModels(
        sessionMaker=Async_Session_Maker,
        DBModels=DBModels,
        jsonData=DemoData,
    )    
    return Async_Session_Maker

@pytest.fixture
def LoadersContext(SQLite):
    from utils.Dataloaders import createLoadersContext
    context = createLoadersContext(SQLite)
    return context

@pytest.fixture
def Context(LoggedUser, SQLite, LoadersContext):
    from utils.gql_ug_proxy import get_ug_connection
    
    Async_Session_Maker = SQLite
    return {
        **LoadersContext,
        "": Async_Session_Maker,
        "u": LoggedUser,
        "x": "",
        "ug_connection": get_ug_connection
    }

@pytest.fixture
def Request():
    class _Request():
        @property
        def headers(self):
            return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
    return _Request()

@pytest.fixture
def Info(Request, Context):
    class _Info():
        @property
        def context(self):
            context = Context
            context["request"] = Request
            return context

    return _Info()

@pytest.fixture
def QueriesFile():
    file = open("queries.txt", "w+", encoding="utf-8")
    def writequery(query=None, mutation=None, variables={}):
        if (query is not None) and ("mutation" in query):
            jsonData = {
                "query": None,
                "mutation": query,
                "variables": variables
            }
        else:
            jsonData = {
                "query": query,
                "mutation": mutation,
                "variables": variables
            }
        rpattern = r"((?:[a-zA-Z]+Insert)|(?:[a-zA-Z]+Update)|(?:[a-zA-Z]+ById)|(?:[a-zA-Z]+Page))"
        qstring = query if query else mutation
        querynames = re.findall(rpattern, qstring)
        print(querynames)
        queryname = queryname if len(querynames) < 1 else "query_" + querynames[0]
        if jsonData.get("query", None) is None:
            queryname = queryname.replace("query", "mutation")
        queryname = queryname + f"_{query.__hash__()}"
        queryname = queryname.replace("-", "")
        line = f'"{queryname}": {json.dumps(jsonData)}, \n'
        file.write(line)
        pass
    try:
        yield writequery
    finally:
        file.close()

@pytest.fixture
def DemoTrue(monkeypatch):
    monkeypatch.setenv("Demo", "True")

@pytest.fixture
def DemoFalse(monkeypatch):
    monkeypatch.setenv("Demo", "False")

@pytest.fixture
def SchemaExecutor(Info, SQLite):
    from GraphTypeDefinitions import schema
    async def Execute(query, variable_values={}):
        result = await schema.execute(query=query, variable_values=variable_values, context_value=Info.context)
        value = {"data": result.data} 
        if result.errors:
            value["errors"] = result.errors
        return value
    return Execute

@pytest.fixture
def SchemaExecutorDemo(DemoTrue, SchemaExecutor):
    return SchemaExecutor

@pytest.fixture
def FastAPIClient(SQLite):
    from fastapi.testclient import TestClient
    import DBDefinitions

    def ComposeCString():
        return "sqlite+aiosqlite:///:memory:"   
    DBDefinitions.ComposeConnectionString = ComposeCString

    import main
    client = TestClient(main.app, raise_server_exceptions=False)   
    return client


@pytest.fixture
def ClientExecutor(FastAPIClient):
    async def Execute(query, variable_values={}):
        json = {
            "query": query,
            "variables": variable_values
        }
        headers = {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        logging.debug(f"query client for {query} with {variable_values}")

        response = FastAPIClient.post("/gql", headers=headers, json=json)
        return response.json()       
    return Execute

@pytest.fixture
def ClientExecutorDemo(DemoTrue, ClientExecutor):
    return ClientExecutor


@pytest.fixture
def LoggedUser(DemoData):
    users = DemoData["users"]
    user = users[0]
    return {**user}

@pytest.fixture
def University(DemoData):
    groups = DemoData["groups"]
    group = next(filter(lambda g: g.get("mastergroup_id", None) is None, groups), None)
    assert group is not None, "group University not found"
    return {**group}

@pytest.fixture
def RoleTypes(DemoData):
    roletypes = DemoData["roletypes"]
    return roletypes

@pytest.fixture
def AllRoleResponse(RoleTypes, LoggedUser, University):
    roletypes = RoleTypes
    allRoles = [
        {"user": {**LoggedUser}, "group": {**University}, "roletype": {**r}}
        for r in roletypes
    ]

    otherroles = [
        {"user": {"id": uuid1()}, "group": {"id": uuid1()}, "roletype": random.choice(roletypes)}
        for i in range(10)
        ]

    response = {"data": {"result": {"roles": [
        *otherroles,
        *allRoles
    ]}}}

    # print("createRoleResponse.result", response)
    return response

@pytest.fixture
def NoRoleResponse(RoleTypes):
    roletypes = RoleTypes
    otherroles = [
        {"user": {"id": uuid1()}, "group": {"id": uuid1()}, "roletype": random.choice(roletypes)}
        for i in range(10)
        ]

    response = {"data": {"result": {"roles": [
        *otherroles,
    ]}}}
    
    #print("NoRoleResponse.result", response)
    return response

@pytest.fixture
def Env_GQLUG_ENDPOINT_URL_8123(monkeypatch):
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL == "http://localhost:8123/gql", "GQLUG_ENDPOINT_URL setup failed"
    return ("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")

@pytest.fixture(autouse=True) # allrole
def Env_GQLUG_ENDPOINT_URL_8124(monkeypatch):
    # print(40*"GQLUG")
    monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8124/gql")
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL == "http://localhost:8124/gql", "GQLUG_ENDPOINT_URL setup failed"
    # print(40*"#")
    return ("GQLUG_ENDPOINT_URL", "http://localhost:8124/gql")

def run(port, response):
    class Item(BaseModel):
        query: str
        variables: dict = None
        operationName: str = None

    app = fastapi.FastAPI()

    @app.post("/gql")
    async def gql_query(item: Item):
        # print("APP queried", item.query)
        #logging.info(f"SERVER Query {item} -> {response}")
        return response
    #print("APP created for", response)

    uvicorn.run(app, port=port)

def runServer(port, response):
    #print(response)
    from multiprocessing import Process
   
    _api_process = Process(target=run, daemon=True, kwargs={"response": response, "port": port})
    _api_process.start()
    print(f"UG_Server started at {port}")
    yield _api_process
    _api_process.terminate()
    _api_process.join()
    print(f"UG_Server stopped at {port}")

@pytest.fixture(autouse=True)
def NoRole_UG_Server(NoRoleResponse):
    yield from runServer(port=8123, response=NoRoleResponse)

@pytest.fixture(autouse=True)
def AllRole_UG_Server(AllRoleResponse):
    yield from runServer(port=8124, response=AllRoleResponse)

