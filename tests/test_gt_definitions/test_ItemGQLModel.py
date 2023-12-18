import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_items = createResolveReferenceTest(tableName='formitems', gqltype='FormItemGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_item_by_id = createByIdTest(tableName="formitems", queryEndpoint="formItemById")
test_query_item_page = createPageTest(tableName="formitems", queryEndpoint="formItemPage")

test_item_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $partId: UUID!) { 
        result: formItemInsert(item: {id: $id, name: $name, partId: $partId}) { 
            id
            msg
            item {
                id
                name
                order
                type { id }
                part { id }
            }
        }
    }
    """, 
    variables={"id": "ee40b3bf-ac51-4dbb-8f73-d5da30bf8017", "name": "new item", "partId": "52e3f2d6-afb1-11ed-9bd8-0242ac110002"},
    asserts=[]
)


test_item_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!, $value: String!) {
            formItemUpdate(item: {id: $id, name: $name, lastchange: $lastchange, value: $value}) {
                id
                msg
                item {
                    id
                    name
                    value
                    lastchange
                }
            }
        }

    """,
    variables={"id": "72a3d4b0-afb1-11ed-9bd8-0242ac110002", "name": "new name", "value": "other value"},
    tableName="formitems"
)
