import json
from typing import Union, Optional, Any
from pydantic import BaseModel, Field, ValidationError


class StateResponseSchema(BaseModel):
    code: Optional[int]
    title: str


class APICategorySchema(BaseModel):
    section_guid: str
    code: int
    title: str
    cover_image: str
    product_qty: int
    is_current: bool
    sections:  Optional["list[APICategorySchema]"]


class GetCategoryAPIResponseSchema(BaseModel):
    state: StateResponseSchema
    data:  dict[str, list[APICategorySchema]] = {"sections": list[APICategorySchema]}


class CategorySchema(BaseModel):
    category_id: int
    name: str
    categories: Union["list[CategorySchema]", list[None]] = Field(alias='children')

example_dict = {
    "state": {
        "code": 2001,
        "title": "OK"
    }
}

ex_json = {
            "section_guid": "43b98880-2f29-11eb-80cb-00155dfe250f",
            "code": 245635348,
            "title": "Стройматериалы",
            "cover_image": "//cs.petrovich.ru/images/1221703/original.jpg",
            "product_qty": 3024,
            "is_current": False,
            "sections": [{
                "section_guid": "e9e4a8f3-e397-11e6-95f7-00259036a192",
                "code": 12101,
                "title": "Стеновые и фасадные материалы",
                "cover_image": "//cs.petrovich.ru/image/6429789/original.jpg",
                "product_qty": 334,
                "is_current": False,
                "sections": [{
                    "section_guid": "e9e4a93f-e397-11e6-95f7-00259036a192",
                    "code": 1557,
                    "title": "Кирпич",
                    "cover_image": "//cs.petrovich.ru/images/1261629/original.jpg",
                    "product_qty": 17,
                    "is_current": False,
                    "sections": None
                }]
            }]
    }


with open('../parser/static/petrovich/petrovich_api_category.json', "r", encoding="utf-8") as outfile:
    my_dict = json.loads(outfile.read())

# j = APICategorySchema.parse_obj(ex_json)
# print(j)
categories_shop_response = GetCategoryAPIResponseSchema.parse_obj(my_dict)

a = CategorySchema(**ex_json)
a.categories.append()

# try:
#     j = APICategorySchema.parse_obj()
# except ValidationError as e:
#     print(e.json())
#
# print(j.json())
