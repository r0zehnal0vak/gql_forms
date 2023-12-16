from typing import Any, List
import logging
import os
from pydantic import BaseModel

import logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')

from fastapi import FastAPI, Request, Depends
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

from DBDefinitions import ComposeConnectionString

## Zabezpecuje prvotni inicializaci DB a definovani Nahodne struktury pro "Univerzity"
# from gql_workflow.DBFeeder import createSystemDataStructureRoleTypes, createSystemDataStructureGroupTypes

connectionString = ComposeConnectionString()

appcontext = {}
@asynccontextmanager
async def initEngine(app: FastAPI):

    from DBDefinitions import startEngine, ComposeConnectionString

    connectionstring = ComposeConnectionString()

    asyncSessionMaker = await startEngine(
        connectionstring=connectionstring,
        makeDrop=True,
        makeUp=True
    )

    appcontext["asyncSessionMaker"] = asyncSessionMaker

    logging.info("engine started")

    from utils.DBFeeder import initDB
    await initDB(asyncSessionMaker)

    logging.info("data (if any) imported")
    yield


from GraphTypeDefinitions import schema

async def get_context(request: Request):
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    from utils.Dataloaders import createLoadersContext, createUgConnectionContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    
    connectionContext = createUgConnectionContext(request=request)
    return {**context, **connectionContext}

app = FastAPI(lifespan=initEngine)

from doc import attachVoyager
attachVoyager(app, path="/gql/doc")

print("All initialization is done")
@app.get('/hello')
def hello(request: Request):
    headers = request.headers
    auth = request.auth
    user = request.scope["user"]
    return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None

@app.get("/gql")
async def graphiql(request: Request):
    return await graphql_app.render_graphql_ide(request)

from utils.sentinel import sentinel

@app.post("/gql")
async def apollo_gql(request: Request, item: Item):
    if not DEMO:
        sentinelResult = await sentinel(request, item)
        if sentinelResult:
            return sentinelResult
    try:
        context = await get_context(request)
        schemaresult = await schema.execute(item.query, variable_values=item.variables, operation_name=item.operationName, context_value=context)
        # assert 1 == 0, ":)"
    except Exception as e:
        return {"data": None, "errors": [f"{type(e).__name__}: {e}"]}
    
    result = {"data": schemaresult.data}
    if schemaresult.errors:
        result["errors"] = [f"{error}" for error in schemaresult.errors]
    return result

# from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
# app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(
#         JWTPUBLICKEY = JWTPUBLICKEY,
#         JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
# ))

import os
DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    print("####################################################")
    print("#                                                  #")
    print("# RUNNING IN DEMO                                  #")
    print("#                                                  #")
    print("####################################################")

    logging.info("####################################################")
    logging.info("#                                                  #")
    logging.info("# RUNNING IN DEMO                                  #")
    logging.info("#                                                  #")
    logging.info("####################################################")

if not DEMO:
    GQLUG_ENDPOINT_URL = os.environ("GQLUG_ENDPOINT_URL", None)
    assert GQLUG_ENDPOINT_URL is not None, "GQLUG_ENDPOINT_URL environment variable must be explicitly defined"
    JWTPUBLICKEY = os.environ("JWTPUBLICKEY", None)
    assert JWTPUBLICKEY is not None, "JWTPUBLICKEY environment variable must be explicitly defined"
    JWTRESOLVEUSERPATH = os.environ("JWTRESOLVEUSERPATH", None)
    assert JWTRESOLVEUSERPATH is not None, "JWTRESOLVEUSERPATH environment variable must be explicitly defined"
