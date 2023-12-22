import pytest
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

test_reference_formtypes = createResolveReferenceTest(tableName='formtypes', gqltype='FormTypeGQLModel', attributeNames=["id", "name", "lastchange"])

test_query_form_type_by_id = createByIdTest(tableName="formtypes", queryEndpoint="formTypeById")
test_query_form_type_page = createPageTest(tableName="formtypes", queryEndpoint="formTypePage")

test_insert_form_type = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!) {
        result: formTypeInsert(formType: {id: $id, name: $name}) {
            id
            msg
            type {
                id
                name
                category { id }
                forms { id }
            }
        }
    }""",
    variables={"id": "f6f79926-ac0e-4833-9a38-4272cae33fa6", "name": "new name"}
)

test_update_form_type = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formTypeUpdate(formType: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            type {
                id
                name
            }
        }
    }""",
    variables={"id": "2e1140f4-afb0-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formtypes"
)