import pytest
from GraphTypeDefinitions import schema

from ..shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

from ..gqlshared import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_formcategories = createResolveReferenceTest(tableName='formcategories', gqltype='FormCategoryGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_form_category_by_id = createByIdTest(tableName="formcategories", queryEndpoint="formCategoryById")
test_query_form_category_page = createPageTest(tableName="formcategories", queryEndpoint="formCategoryPage")

test_insert_form_category = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: formCategoryInsert(formCategory: {id: $id, name: $name}) {
            id
            msg
            category {
                id
                name
            }
        }
    }""",
    variables={"id": "fc7f95b5-410c-4a26-a4e9-6b0b2a841645", "name": "new name"}
)

test_update_form_category = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formCategoryUpdate(formCategory: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            category {
                id
                name
            }
        }
    }""",
    variables={"id": "37675bd4-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formcategories"
)