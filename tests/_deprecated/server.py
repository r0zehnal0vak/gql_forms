# import fastapi
# import uvicorn
# import logging
# import asyncio
# from pydantic import BaseModel
# import pytest
# from subprocess import Popen, PIPE
# from http.client import HTTPConnection

# def createServerWithFixedResponse(response: dict):
#     class Item(BaseModel):
#         query: str
#         variables: dict = None
#         operationName: str = None

#     app = fastapi.FastAPI()

#     @app.post("/gql")
#     async def gql_query(item: Item):
#         print("APP queried", item)
#         logging.info(f"SERVER Query {item} -> {response}")
#         return response
#     print("APP created")
#     return app
# import contextlib

# def run(response={}):
#     print(response)
#     app = createServerWithFixedResponse(response=response)
#     uvicorn.run(app, port=8123)

# @contextlib.contextmanager
# def runServer(response: dict = {"hello": "world"}):
#     from multiprocessing import Process
   
#     _api_process = Process(target=run, daemon=True, kwargs={"response": response})
#     _api_process.start()

#     yield 

#     _api_process.terminate()
#     _api_process.join()

# def createStaticServerAsFixture(response: dict = {"hello": "world"}):
#     @pytest.fixture()
#     def static_server():

#         app = createServerWithFixedResponse(response=response)
#         config = uvicorn.Config(app, host='0.0.0.0', port=8123)
#         server = uvicorn.Server(config)
#         # server.should_exit = True
#         server.serve()
#         # task = asyncio.create_task(server.startup())
#         # return task

#         return server
        
#     return static_server

# def run(response={}):
#     print(response)
#     app = createServerWithFixedResponse(response=response)
#     uvicorn.run(app, port=8123)

# def run(response):
#     class Item(BaseModel):
#         query: str
#         variables: dict = None
#         operationName: str = None

#     app = fastapi.FastAPI()

#     @app.post("/gql")
#     async def gql_query(item: Item):
#         print("APP queried", item)
#         logging.info(f"SERVER Query {item} -> {response}")
#         return response
#     print("APP created for", response)

#     uvicorn.run(app, port=8123)

# @pytest.fixture
# def Env_GQLUG_ENDPOINT_URL(monkeypatch):
#     monkeypatch.setenv("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")
#     return ("GQLUG_ENDPOINT_URL", "http://localhost:8123/gql")

# @pytest.fixture
# def UG_Server(request, Env_GQLUG_ENDPOINT_URL):
#     print(request)
#     from multiprocessing import Process
   
#     _api_process = Process(target=run, daemon=True, kwargs={"response": request.param})
#     _api_process.start()
#     print("UG_Server started")
#     yield _api_process
#     _api_process.terminate()
#     _api_process.join()
#     print("UG_Server stopped")

#     pass

# @contextlib.contextmanager
# def runServer(response: dict = {"hello": "world"}):
#     from multiprocessing import Process
   
#     _api_process = Process(target=run, daemon=True, kwargs={"response": response})
#     _api_process.start()

#     yield 

#     _api_process.terminate()
#     _api_process.join()
