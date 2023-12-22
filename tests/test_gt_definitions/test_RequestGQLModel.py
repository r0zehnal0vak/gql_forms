import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_requests = createResolveReferenceTest(tableName='formrequests', gqltype='RequestGQLModel')
test_query_request_by_id = createByIdTest(tableName="formrequests", queryEndpoint="requestById")
test_query_request_page = createPageTest(tableName="formrequests", queryEndpoint="requestPage")

test_resolve_request = createResolveReferenceTest('formrequests', 'RequestGQLModel', ['id', 'lastchange'])

test_insert_request = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: formRequestInsert(request: {id: $id, name: $name}) {
            id
            msg
            request {
                id
                name
                creator { id }
                histories { id }
                
            }
        }
    }""",
    variables={"id": "7442f283-f66f-46da-90b2-aa334439c8f6", "name": "new name"}
)

test_update_request = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formRequestUpdate(request: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            request {
                id
                name
            }
        }
    }""",
    variables={"id": "13181566-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formrequests"
)