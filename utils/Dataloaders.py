from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
from functools import cache
import logging

from DBDefinitions import (
    FormModel, 
    FormTypeModel, 
    FormCategoryModel,
    RequestModel, 
    HistoryModel,
    SectionModel, 
    PartModel,
    ItemModel, 
    ItemTypeModel, 
    ItemCategoryModel
)

async def createLoaders_3(asyncSessionMaker):

    class Loaders:
        @property
        @cache
        def request_by_id(self):
            return createIdLoader(asyncSessionMaker, RequestModel)

        @property
        @cache
        def requests_by_createdby(self):
            return createFkeyLoader(asyncSessionMaker, RequestModel, foreignKeyName="createdby")

        @property
        @cache
        def form_by_id(self):
            return createIdLoader(asyncSessionMaker, FormModel)

        @property
        @cache
        def formtype_by_id(self):
            return createIdLoader(asyncSessionMaker, FormTypeModel)

        @property
        @cache
        def formcategory_by_id(self):
            return createIdLoader(asyncSessionMaker, FormCategoryModel)

        @property
        @cache
        def history_by_id(self):
            return createIdLoader(asyncSessionMaker, HistoryModel)

        @property
        @cache
        def histories_by_request_id(self):
            return createFkeyLoader(asyncSessionMaker, HistoryModel, foreignKeyName="request_id")

        @property
        @cache
        def section_by_id(self):
            return createIdLoader(asyncSessionMaker, SectionModel)

        @property
        @cache
        def section_by_form_id(self):
            return createFkeyLoader(asyncSessionMaker, SectionModel, foreignKeyName="form_id")

        @property
        @cache
        def part_by_id(self):
            return createIdLoader(asyncSessionMaker, PartModel)

        @property
        @cache
        def parts_by_section_id(self):
            return createFkeyLoader(asyncSessionMaker, PartModel, foreignKeyName="section_id")

        @property
        @cache
        def item_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemModel)

        @property
        @cache
        def item_type_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemTypeModel)

        @property
        @cache
        def item_category_by_id(self):
            return createIdLoader(asyncSessionMaker, ItemCategoryModel)

        @property
        @cache
        def items_by_part_id(self):
            return createFkeyLoader(asyncSessionMaker, ItemModel, foreignKeyName="part_id")

        # @property
        # @cache
        # def facilities_by_master_id(self):
        #     return createFkeyLoader(asyncSessionMaker, FacilityModel, foreignKeyName="master_facility_id")
    return Loaders()



dbmodels = {
    "forms": FormModel, 
    "formtypes": FormTypeModel, 
    "formcategories": FormCategoryModel,
    "requests": RequestModel, 
    "histories": HistoryModel,
    "sections": SectionModel, 
    "parts": PartModel,
    "items": ItemModel, 
    "itemtypes": ItemTypeModel, 
    "itemcategories": ItemCategoryModel
}

async def createLoaders(asyncSessionMaker, models=dbmodels):
    def createLambda(loaderName, DBModel):
        return lambda self: createIdLoader(asyncSessionMaker, DBModel)
    
    attrs = {}
    for key, DBModel in models.items():
        attrs[key] = property(cache(createLambda(key, DBModel)))
    
    Loaders = type('Loaders', (), attrs)   
    return Loaders()

class Loaders:
    requests = None
    histories = None
    forms = None
    formtypes = None
    formcategories = None
    sections = None
    parts = None
    items = None
    itemtypes = None
    itemcategories = None
    pass

def createLoaders(asyncSessionMaker, models=dbmodels) -> Loaders:
    class Loaders:
        @property
        @cache
        def requests(self):
            return createIdLoader(asyncSessionMaker, RequestModel)
        
        @property
        @cache
        def histories(self):
            return createIdLoader(asyncSessionMaker, HistoryModel)
        
        @property
        @cache
        def forms(self):
            return createIdLoader(asyncSessionMaker, FormModel)
        
        @property
        @cache
        def formtypes(self):
            return createIdLoader(asyncSessionMaker, FormTypeModel)
        
        @property
        @cache
        def formcategories(self):
            return createIdLoader(asyncSessionMaker, FormCategoryModel)
        
        @property
        @cache
        def sections(self):
            return createIdLoader(asyncSessionMaker, SectionModel)

        @property
        @cache
        def parts(self):
            return createIdLoader(asyncSessionMaker, PartModel)
        
        @property
        @cache
        def items(self):
            return createIdLoader(asyncSessionMaker, ItemModel)
        
        @property
        @cache
        def itemtypes(self):
            return createIdLoader(asyncSessionMaker, ItemTypeModel)

        @property
        @cache
        def itemcategories(self):
            return createIdLoader(asyncSessionMaker, ItemCategoryModel)
        
    return Loaders()


def getLoadersFromInfo(info) -> Loaders:
    context = info.context
    loaders = context["loaders"]
    return loaders

from functools import cache


demouser = {
    "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
    "name": "John",
    "surname": "Newbie",
    "email": "john.newbie@world.com",
    "roles": [
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                "name": "administrátor"
            }
        },
        {
            "valid": True,
            "group": {
                "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                "name": "Uni"
            },
            "roletype": {
                "id": "ae3f0d74-6159-11ed-b753-0242ac120003",
                "name": "rektor"
            }
        }
    ]
}

def getUserFromInfo(info):
    context = info.context
    #print(list(context.keys()))
    result = context.get("user", None)
    if result is None:
        authorization = context["request"].headers.get("Authorization", None)
        if authorization is not None:
            if 'Bearer ' in authorization:
                token = authorization.split(' ')[1]
                if token == "2d9dc5ca-a4a2-11ed-b9df-0242ac120003":
                    result = demouser
                    context["user"] = result
    logging.debug("getUserFromInfo", result)
    return result

def createLoadersContext(asyncSessionMaker):
    return {
        "loaders": createLoaders(asyncSessionMaker)
    }
