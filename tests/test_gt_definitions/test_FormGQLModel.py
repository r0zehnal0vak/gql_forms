import pytest
# import os
# os.environ["GQLUG_ENDPOINT_URL"] = "http://localhost:8124/gql"
# print(os.environ.get("GQLUG_ENDPOINT_URL", None))


# from ..gqlshared import (
#     createByIdTest, 
#     createPageTest, 
#     createResolveReferenceTest, 
#     createFrontendQuery, 
#     createUpdateQuery
# )

from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_forms = createResolveReferenceTest(
    tableName='forms', gqltype='FormGQLModel', 
    attributeNames=["id", "name", "lastchange", "valid", "status", "creator {id}", "nameEn", "createdby {id}"])
test_query_form_by_id = createByIdTest(tableName="forms", queryEndpoint="formById")
test_query_form_page = createPageTest(tableName="forms", queryEndpoint="formPage")


test_form_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $rbac_id: UUID!) { 
        result: formInsert(form: {id: $id, name: $name, rbacobject: $rbac_id}) { 
            id
            msg
            form {
                id
                name
                type { id }

                lastchange
                created
                changedby { id }
                rbacobject { id }                
            }
        }
    }
    """, 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3", "name": "new form", "rbac_id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003"},
    asserts=[]
)



test_form_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            formUpdate(form: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                form {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="forms"
)



test_form_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            formUpdate(form: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                form {
                    id
                    name
                }
            }
        }
    """,
    variables={"id": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="forms"
)

test_hello_forms = createFrontendQuery(query="""
    query($id: UUID!){ sayHelloForms(id: $id) }""", 
    variables={"id": "ccde3a8b-81d0-4e2b-9aac-42e0eb2255b3"},
    asserts=[]
)

