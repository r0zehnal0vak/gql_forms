import pytest
from .gt_utils import (
    createByIdTest, 
    createPageTest, 
    createResolveReferenceTest, 
    createFrontendQuery, 
    createUpdateQuery
)

test_reference_parts = createResolveReferenceTest(tableName='formparts', gqltype='FormPartGQLModel', attributeNames=["id", "name", "lastchange", "order", "section {id}"])
test_resolve_part = createResolveReferenceTest('formparts', 'FormPartGQLModel', ['id', 'lastchange', 'order'])


test_part_insert = createFrontendQuery(query="""
    mutation($id: UUID!, $name: String!, $section_id: UUID!) { 
        result: formPartInsert(part: {id: $id, name: $name, sectionId: $section_id}) { 
            id
            msg
            part {
                id
                name
                items { id }
            }
        }
    }
    """, 
    variables={"id": "53365ad1-acce-4c29-b0b9-c51c67af4033", "name": "new part", "section_id": "48bbc7d4-afb1-11ed-9bd8-0242ac110002"},
    asserts=[]
)


test_part_update = createUpdateQuery(
    query="""
        mutation($id: UUID!, $name: String!, $lastchange: DateTime!) {
            formPartUpdate(part: {id: $id, name: $name, lastchange: $lastchange}) {
                id
                msg
                part {
                    id
                    name
                    lastchange
                }
            }
        }

    """,
    variables={"id": "52e3ee26-afb1-11ed-9bd8-0242ac110002", "name": "new name"},
    tableName="formparts"
)