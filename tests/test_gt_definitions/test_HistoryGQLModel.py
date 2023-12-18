import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_histories = createResolveReferenceTest(tableName='formhistories', gqltype='RequestHistoryGQLModel')

test_insert_history = createFrontendQuery(
    query="""mutation ($id: UUID!, $name: String!, $request_id: UUID!, $form_id: UUID!) {
        result: formHistoryInsert(history: {id: $id, name: $name, requestId: $request_id, formId: $form_id}) {
            id
            msg
            history {
                id
                name
                form { id }
                request { id }
            }
        }
    }""",
    variables={
        "id": "4d8fdcb1-bde1-47da-80bb-a67917e1914a", 
        "name": "new name",
        "request_id": "13181566-afb0-11ed-9bd8-0242ac110002", 
        "form_id": "190d578c-afb1-11ed-9bd8-0242ac110002",
    }
)

test_update_history = createUpdateQuery(
    query="""mutation ($id: UUID!, $name: String!, $lastchange: DateTime!) {
        result: formHistoryUpdate(history: {id: $id, name: $name, lastchange: $lastchange}) {
            id
            msg
            history {
                id
                name
            }
        }
    }""",
    variables={"id": "84c35266-afb5-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formhistories"
)