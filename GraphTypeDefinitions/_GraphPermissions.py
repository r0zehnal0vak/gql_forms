from sqlalchemy.future import select
import strawberry
from typing import List
from uuid import UUID


def AsyncSessionFromInfo(info):
    return info.context["session"]


def UserFromInfo(info):
    return info.context["user"]


class BasePermission(strawberry.permission.BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("BasePermission", source)
        print("BasePermission", self)
        print("BasePermission", kwargs)
        return True


from functools import cache
import aiohttp


rolelist = [
        {
            "name": "já",
            "name_en": "myself",
            "id": "05a3e0f5-f71e-4caa-8012-229d868aa8ca",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "administrátor",
            "name_en": "administrator",
            "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
            "category_id": "774690a0-56b3-45d9-9887-0989ed3de4c0"
        },
        {
            "name": "zpracovatel gdpr",
            "name_en": "gdpr user",
            "id": "b87aed46-dfc3-40f8-ad49-03f4138c7478",
            "category_id": "774690a0-56b3-45d9-9887-0989ed3de4c0"
        },
        {
            "name": "rektor",
            "name_en": "rector",
            "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "prorektor",
            "name_en": "vicerector",
            "id": "ae3f2886-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "děkan",
            "name_en": "dean",
            "id": "ae3f2912-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "proděkan",
            "name_en": "vicedean",
            "id": "ae3f2980-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "vedoucí katedry",
            "name_en": "head of department",
            "id": "ae3f29ee-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "vedoucí učitel",
            "name_en": "leading teacher",
            "id": "ae3f2a5c-6159-11ed-b753-0242ac120003",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant",
            "name_en": "grant",
            "id": "5f0c247e-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant (zástupce)",
            "name_en": "grant (deputy)",
            "id": "5f0c2532-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "garant předmětu",
            "name_en": "subject's grant",
            "id": "5f0c255a-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "přednášející",
            "name_en": "lecturer",
            "id": "5f0c2578-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        },
        {
            "name": "cvičící",
            "name_en": "trainer",
            "id": "5f0c2596-931f-11ed-9b95-0242ac110002",
            "category_id": "fd73596b-1043-46f0-837a-baa0734d64df"
        }
    ]

roleIndex = { role["name_en"]: role["id"] for role in rolelist }

import requests
def ReadRolesSync(
    userId="2d9dc5ca-a4a2-11ed-b9df-0242ac120003", 
    roleUrlEndpoint="http://localhost:8088/gql/"    
    ):

    query = """query($userid: UUID!){
            roles: roleByUser(userId: $userid) {
                id
                valid
                roletype { id }
                group { id }
                user { id }
            }
        }
"""
    variables = {"userid": userId}
    headers = {}
    json = {
        "query": query,
        "variables": variables
    }

    response = requests.post(url=roleUrlEndpoint, json=json, headers=headers)
    respJson = response.json()
    assert respJson.get("errors", None) is None
    respdata = respJson.get("data", None)
    assert respdata is not None
    roles = respdata.get("roles", None)
    assert roles is not None
    print("roles", roles)
    return [*roles]

async def ReadRoles(
    userId="2d9dc5ca-a4a2-11ed-b9df-0242ac120003", 
    roleUrlEndpoint="http://localhost:8088/gql/"):
    
    query = """query($userid: UUID!){
            roles: roleByUser(userId: $userid) {
                id
                valid
                roletype { id }
                group { id }
                user { id }
            }
        }
"""
    variables = {"userid": userId}
    headers = {}
    json = {
        "query": query,
        "variables": variables
    }

    print("roleUrlEndpoint", roleUrlEndpoint)
    async with aiohttp.ClientSession() as session:
        print(f"query {roleUrlEndpoint} for json={json}")
        async with session.post(url=roleUrlEndpoint, json=json, headers=headers) as resp:
            print(resp.status)
            if resp.status != 200:
                text = await resp.text()
                print(text)
                return []
            else:
                respJson = await resp.json()

    print(respJson)
    
    assert respJson.get("errors", None) is None
    respdata = respJson.get("data", None)
    assert respdata is not None
    roles = respdata.get("roles", None)
    assert roles is not None
    print("roles", roles)
    return [*roles]


def RoleBasedPermission(roles: str = ""):
    roleNames = roles.split(";")
    roleNames = list(map(lambda item: item.strip(), roleNames))
    rolesNeeded = list(map(lambda item: roleIndex[item], roleNames))
    class RolebasedPermission(BasePermission):
        message = "User has not appropriate roles"

        async def has_permission(
            self, source, info: strawberry.types.Info, **kwargs
        ) -> bool:
            context = info.context
            roles = context["userroles"]
            print("GroupEditorPermission", source)
            print("GroupEditorPermission", self)
            print("GroupEditorPermission", kwargs)
            # _ = await self.canEditGroup(session,  source.id, ...)
            print("GroupEditorPermission")
            
            print(roles)
            print(rolesNeeded)
            return True
        
    return RolebasedPermission


class UserGDPRPermission(BasePermission):
    message = "User is not authenticated"

    async def has_permission(
        self, source, info: strawberry.types.Info, **kwargs
    ) -> bool:
        print("UserGDPRPermission", source)
        print("UserGDPRPermission", self)
        print("UserGDPRPermission", kwargs)
        return True
