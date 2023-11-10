import logging
import sqlalchemy
import sys
import asyncio

import pytest

from GraphTypeDefinitions import schema

from .shared import (
    prepare_demodata,
    prepare_in_memory_sqllite,
    get_demodata,
    createContext,
)

def createByIdTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()
        datarow = data[tableName][0]
        content = "{" + ", ".join(attributeNames) + "}"
        query = "query($id: UUID!){" f"{queryEndpoint}(id: $id)" f"{content}" "}"

        context_value = createContext(async_session_maker)
        variable_values = {"id": f'{datarow["id"]}'}
        
        logging.debug(f"query for {query} with {variable_values}")

        resp = await schema.execute(
            query, context_value=context_value, variable_values=variable_values
        )

        respdata = resp.data[queryEndpoint]

        assert resp.errors is None

        for att in attributeNames:
            assert respdata[att] == f'{datarow[att]}'

    return result_test


def createPageTest(tableName, queryEndpoint, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        data = get_demodata()

        content = "{" + ", ".join(attributeNames) + "}"
        query = "query{" f"{queryEndpoint}" f"{content}" "}"

        context_value = createContext(async_session_maker)
        logging.debug(f"query for {query}")

        resp = await schema.execute(query, context_value=context_value)

        respdata = resp.data[queryEndpoint]
        datarows = data[tableName]

        assert resp.errors is None

        for rowa, rowb in zip(respdata, datarows):
            for att in attributeNames:
                assert rowa[att] == f'{rowb[att]}'

    return result_test

def createResolveReferenceTest(tableName, gqltype, attributeNames=["id", "name"]):
    @pytest.mark.asyncio
    async def result_test():
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)

        content = "{" + ", ".join(attributeNames) + "}"

        data = get_demodata()
        table = data[tableName]
        for row in table:
            rowid = f"{row['id']}"

            query = (
                'query($id: UUID!) { _entities(representations: [{ __typename: '+ f'"{gqltype}", id: $id' + 
                ' }])' +
                '{' +
                f'...on {gqltype}' + content +
                '}' + 
                '}')

            context_value = createContext(async_session_maker)
            variable_values = {"id": rowid}
            #variable_values = {"id", row['id']}
            logging.info(f"query for {query} with {variable_values}")
            resp = await schema.execute(query, context_value=context_value, variable_values=variable_values)
            data = resp.data
            logging.info(data)
            data = data['_entities'][0]

            assert data['id'] == rowid

    return result_test

def createFrontendQuery(query="{}", variables={}, asserts=[]):
    @pytest.mark.asyncio
    async def test_frontend_query():    
        logging.debug("createFrontendQuery")
        async_session_maker = await prepare_in_memory_sqllite()
        await prepare_demodata(async_session_maker)
        context_value = createContext(async_session_maker)
        logging.debug(f"query for {query} with {variables}")
        resp = await schema.execute(
            query=query, 
            variable_values=variables, 
            context_value=context_value
        )

        assert resp.errors is None
        respdata = resp.data
        logging.debug(f"response: {respdata}")
        for a in asserts:
            a(respdata)
    return test_frontend_query
