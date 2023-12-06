from typing import List
import logging

import logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s', 
    datefmt='%Y-%m-%dT%I:%M:%S')

from fastapi import FastAPI, Request
import strawberry
from strawberry.fastapi import GraphQLRouter
from contextlib import asynccontextmanager

## Definice GraphQL typu (pomoci strawberry https://strawberry.rocks/)
## Strawberry zvoleno kvuli moznosti mit federovane GraphQL API (https://strawberry.rocks/docs/guides/federation, https://www.apollographql.com/docs/federation/)
from GraphTypeDefinitions import Query

## Definice DB typu (pomoci SQLAlchemy https://www.sqlalchemy.org/)
## SQLAlchemy zvoleno kvuli moznost komunikovat s DB asynchronne
## https://docs.sqlalchemy.org/en/14/core/future.html?highlight=select#sqlalchemy.future.select
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

async def get_context():
    asyncSessionMaker = appcontext.get("asyncSessionMaker", None)
    if asyncSessionMaker is None:
        async with initEngine(app) as cntx:
            pass
        
    from utils.Dataloaders import createLoadersContext
    context = createLoadersContext(appcontext["asyncSessionMaker"])
    return {**context}

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

def createApp():
    app = FastAPI(lifespan=initEngine)
    app.include_router(graphql_app, prefix="/gql")

    from doc import attachVoyager
    attachVoyager(app, path="/gql/doc")

    print("All initialization is done")
    @app.get('/hello')
    def hello(request: Request):
        headers = request.headers
        auth = request.auth
        user = request.scope["user"]
        return {'hello': 'world', 'headers': {**headers}, 'auth': f"{auth}", 'user': user}
    return app

app = createApp()
import os
JWTPUBLICKEY = os.environ.get("JWTPUBLICKEY", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATH = os.environ.get("JWTRESOLVEUSERPATH", "http://localhost:8000/oauth/userinfo")

from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
app.add_middleware(BasicAuthenticationMiddleware302, backend=BasicAuthBackend(
        JWTPUBLICKEY = JWTPUBLICKEY,
        JWTRESOLVEUSERPATH = JWTRESOLVEUSERPATH
))

import os
demo = os.getenv("DEMO", None)
print("DEMO", demo, type(demo))
demo = os.getenv("DEMOUSER", None)
print("DEMOUSER", demo, type(demo))