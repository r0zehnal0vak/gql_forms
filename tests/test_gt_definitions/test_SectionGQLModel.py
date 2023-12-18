import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_sections = createResolveReferenceTest(tableName='formsections', gqltype='FormSectionGQLModel', attributeNames=["id", "name", "lastchange"])
test_resolve_section = createResolveReferenceTest('formsections', 'FormSectionGQLModel', ['id', 'lastchange'])


test_insert_section = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $formid: UUID!) {
        result: formSectionInsert(section: {id: $id, name: $name, formId: $formid}) {
            id
            msg
            section {
                id
                name
                order
                form {
                    id
                }
                parts {
                    id
                }
            }
        }
    }""",
    variables={"id": "59e7d0b2-7a0b-4b5a-82ec-aff0c836d45a", "formid": "190d578c-afb1-11ed-9bd8-0242ac110002", "name": "new name"}
)

test_update_section = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formSectionUpdate(section: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            section {
                id
                name
            }
        }
    }""",
    variables={"id": "48bbc7d4-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formsections"
)