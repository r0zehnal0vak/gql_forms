import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_itemcategories = createResolveReferenceTest(tableName='formitemcategories', gqltype='FormItemCategoryGQLModel')

test_query_item_category_by_id = createByIdTest(tableName="formitemcategories", queryEndpoint="itemCategoryById")
test_query_item_category_page = createPageTest(tableName="formitemcategories", queryEndpoint="itemCategoryPage")

test_insert_item_category = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: formItemCategoryInsert(itemCategory: {id: $id, name: $name}) {
            id
            msg
            category {
                id
                name
                types { id }
            }
        }
    }""",
    variables={"id": "e1298bc1-adfc-445f-8ac7-977b1ffd2efb", "name": "new name"}
)

test_update_item_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formItemCategoryUpdate(itemCategory: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            category {
                id
                name
            }
        }
    }""",
    variables={"id": "b1cb0f80-afb8-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formitemcategories"
)