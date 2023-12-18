import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_itemtypes = createResolveReferenceTest(tableName='formitemtypes', gqltype='FormItemTypeGQLModel', attributeNames=["id", "items {id}"])

test_query_item_type_by_id = createByIdTest(tableName="formitemtypes", queryEndpoint="formItemTypeById")
test_query_item_type_page = createPageTest(tableName="formitemtypes", queryEndpoint="formItemTypePage")



test_item_type_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!) { 
        result: formItemTypeInsert(itemType: {id: $id, name: $name}) { 
            id
            msg
            itemType {
                id
                name
                category { id }
            }
        }
    }
    """, 
    variables={"id": "53365ad1-acce-4c29-b0b9-c51c67af4033", "name": "new type"},
    asserts=[]
)


test_item_type_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            formItemTypeUpdate(itemType: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                itemType {
                    id
                    name
                    lastchange
                }
            }
        }

    """,
    variables={"id": "9bdb916a-afb6-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formitemtypes"
)