import logging
import os
import uuid

def uuidstr():
    return f"{uuid.uuid1()}"

# import random
# import pytest
# import aiohttp
# import asyncio
# import uvicorn

# from dataclasses import dataclass
# from uuid import uuid1 as uuid

# from utils.Dataloaders import createLoadersContext

# user = {
#     "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
#     "name": "John",
#     "surname": "Newbie",
#     "email": "john.newbie@world.com"
# }

# def createContext(asyncSessionMaker, user=None):
#     loadersContext = createLoadersContext(asyncSessionMaker)
#     if user:
#         loadersContext["user"] = user
    
#     return loadersContext

# def createInfo(asyncSessionMaker, user=None):
#     class Request():
#         @property
#         def headers(self):
#             return {"Authorization": "Bearer 2d9dc5ca-a4a2-11ed-b9df-0242ac120003"}
        
#     class Info():
#         @property
#         def context(self):
#             context = createContext(asyncSessionMaker, user=user)
#             context["request"] = Request()
#             return context
        
#     return Info()

# def createEntityWithRbacobject(rbacvalue):
#     @dataclass
#     class Entity:
#         rbacobject=rbacvalue
#     return Entity()

# def createConnectionFactory(response):
#     class Connection:
#         async def asyncpost(self, query, variables):
#             return response
#     result = lambda: Connection()
#     return result

# def uuid1():
#     return f"{uuid()}"

# def createRoleResponse(user={"id": ""}, group={"id": ""}, roletype={"id": ""}):
#     from ..shared import get_demodata
#     db = get_demodata()
#     roletypes = db["roletypes"]

#     otherroles = [
#         {"user": {"id": uuid1()}, "group": {"id": uuid1()}, "roletype": random.choice(roletypes)}
#         for i in range(10)
#         ]

#     response = {"data": {"result": {"roles": [
#         *otherroles,
#         {"user": user, "group": group, "roletype": roletype}
#     ]}}}
#     print("createRoleResponse.result", response)
#     return response

# def createConnectionWithAuthorizedResult(user_id, roletype_id):
#     response = createRoleResponse(user={"id": user_id}, group={"id": uuid1()}, roletype={"id": roletype_id})
#     return createConnectionFactory(response)

# def createConnectionWithUnAuthorizedResult(user_id, roletype_id):
#     response = createRoleResponse(user={"id": uuid1()}, group={"id": uuid1()}, roletype={"id": uuid1()})
#     return createConnectionFactory(response)

# from ..server import createStaticServerAsFixture, runServer
# # @pytest.mark.asyncio
# # async def test_server_ok(event_loop):
# #     async def queryServer():
# #         payload = {"query": "", "variables": {}}
# #         async with aiohttp.ClientSession() as session:
# #             async with session.post("http://localhost:8123/gql", json=payload) as response:
# #                 respJson = await response.json()
# #         print("respJson", respJson)
# #         return respJson

# #     with runServer(response= {"hello": "world from here"}) as _:
# #         result = await queryServer()
# #         print(result)

# #     assert True, "I am not ok"
# #     print("DONE")  
# #     assert False

# #     pass
# from ..server import UG_Server, Env_GQLUG_ENDPOINT_URL
# resp = createRoleResponse()

# @pytest.mark.asyncio
# async def test_server_ok(Env_GQLUG_ENDPOINT_URL_8124, AllRole_UG_Server):
#     GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)

#     async def queryServer():
#         payload = {"query": "", "variables": {}}
#         async with aiohttp.ClientSession() as session:
#             async with session.post(GQLUG_ENDPOINT_URL, json=payload) as response:
#                 respJson = await response.json()
#         print("respJson", respJson)
#         return respJson

    
#     print(30*"#")
#     print(GQLUG_ENDPOINT_URL)
#     print(30*"#")
#     result = await queryServer()
#     print(result)

#     assert True, "I am not ok"
#     print("DONE")  
#     # assert False

#     pass

# # from GraphTypeDefinitions import RoleBasedPermission
# # @pytest.mark.asyncio
# # async def test_rbac():
# #     rbacvalue = uuid() # uuid type
# #     user_id = uuid1() # str type
# #     selfObject = createEntityWithRbacobject(rbacvalue)
# #     infoObject = createInfo(None, user={"id": user_id})
# #     connectionFactory=createConnectionWithAuthorizedResult(user_id=user_id)
# #     permissionClass = RoleBasedPermission(roles="", connectionFactory=connectionFactory)
# #     permissionTester = permissionClass()
# #     testResult = await permissionTester.has_permission(source=selfObject, info=infoObject)
# #     assert testResult, "have to be True"
# #     pass

from .gt_utils import createFrontendQuery
_test_request_permitted = createFrontendQuery(
    query="""query ($id: UUID!) {
        requestById(id: $id) {
            id
            name
            permitted
            creator { id }
            histories { id }
        }
    }""",
    variables={"id": "13181566-afb0-11ed-9bd8-0242ac110002"}
)

# def test_raise(AccessToken):
#     print(AccessToken)
#     assert False

import pytest

@pytest.mark.asyncio
async def test_low_role_say_hello(DemoFalse, OAuthServer, ClientExecutorNoDemo, Env_GQLUG_ENDPOINT_URL_8123):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: sayHelloForms(id: $id)
    }
    """
    variable_values = {"id": "190d578c-afb1-11ed-9bd8-0242ac110002"}
    result = await ClientExecutorNoDemo(query=query, variable_values=variable_values)
    logging.info(f"test_low_role_say_hello: \n {result}")
    print(result)
    errors = result.get("errors", None)
    assert errors is None, result




@pytest.mark.asyncio
async def test_demo_role(DemoFalse, ClientExecutorAdmin, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8124):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: formById(id: $id) { 
            id           
        }
    }
    """
    variable_values = {"id": "190d578c-afb1-11ed-9bd8-0242ac110002"}
    result = await ClientExecutorAdmin(query=query, variable_values=variable_values)
    logging.info(f"test_demo_role result: \n {result}")
    print(result)
    errors = result.get("errors", None)
    data = result.get("data", None)
    assert errors is None, result
    assert data["result"] is not None, data
    assert data["result"]["id"] == variable_values["id"], data
    

@pytest.mark.asyncio
async def test_low_role(DemoFalse, ClientExecutorNoAdmin, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8124):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: formById(id: $id) { 
            id           
        }
    }
    """
    variable_values = {"id": "190d578c-afb1-11ed-9bd8-0242ac110002"}
    result = await ClientExecutorNoAdmin(query=query, variable_values=variable_values)
    logging.info(f"test_demo_role result: \n {result}")
    print(result)
    errors = result.get("errors", None)
    data = result.get("data", None)
    assert errors is None, result
    assert data["result"] is not None, data
    assert data["result"]["id"] == variable_values["id"], data
    

@pytest.mark.asyncio
async def test_low_role2(DemoFalse, ClientExecutorNoAdmin2, FillDataViaGQL, Context, Env_GQLUG_ENDPOINT_URL_8123):
    GQLUG_ENDPOINT_URL = os.environ.get("GQLUG_ENDPOINT_URL", None)
    logging.info(f"test_low_role GQLUG_ENDPOINT_URL: \n{GQLUG_ENDPOINT_URL}")
    DEMO = os.environ.get("DEMO", None)
    logging.info(f"test_low_role DEMO: {DEMO}")
    query = """
    query($id: UUID!) { 
        result: formById(id: $id) { 
            id          
            sections { id } 
        }
    }
    """
    variable_values = {"id": "190d578c-afb1-11ed-9bd8-0242ac110002"}
    result = await ClientExecutorNoAdmin2(query=query, variable_values=variable_values)
    logging.info(f"test_demo_role got for query \n {query} \n\t with variables \n {variable_values} \n\t the result: \n {result}")
    print(result)
    errors = result.get("errors", None)
    data = result.get("data", None)
    assert errors is None, result
    assert data is not None, data
    assert data.get("result", None) is not None, data
    assert data["result"].get("id", None) == variable_values["id"], data
        