from dataclasses import dataclass

from fastapi import Query
from pydantic import BaseModel

from directory.territories import docs
from directory.territories.enums import KATOTTGCategory, KOATUUCategory


@dataclass
class ListParametersBase:
    page: int = Query(default=1, gte=1, description="Номер сторінки")
    page_size: int = Query(
        default=20,
        gt=1,
        lte=100,
        description="Кількість елементів на сторінці",
    )

    @property
    def limit(self) -> int:
        return self.page_size + 1

    @property
    def offset(self) -> int:
        return self.page_size * (self.page - 1)


class ListResponseBase(BaseModel):
    has_next: bool
    has_previous: bool
    page: int


class KATOTTG(BaseModel):
    code: str
    name: str
    name_en: str
    level: int
    parent_id: str | None
    category: KATOTTGCategory
    children_count: int

    class Config:
        orm_mode = True


class KOATUU(BaseModel):
    code: str
    category: KOATUUCategory | None
    name: str
    name_en: str
    katottg_code: str | None
    katottg_name: str | None
    katottg_category: KATOTTGCategory | None

    class Config:
        orm_mode = True


@dataclass
class GetKATOTTGListParams(ListParametersBase):
    code: str | None = Query(default=None, description="Фільтр по коду КАТОТТГ")
    name: str | None = Query(default=None, description="Фільтр по назві території")
    level: int | None = Query(default=None, description="Фільтр по рівню території")
    parent: str | None = Query(
        default=None,
        description="Фільтр по коду КАТОТТГ території вищого рівня",
    )
    category: KATOTTGCategory | None = Query(
        default=None,
        description="Фільтр по категорії території",
    )


@dataclass
class GetKOATUUGListParams(ListParametersBase):
    code: str | None = Query(default=None)
    name: str | None = Query(default=None)
    category: KOATUUCategory | None = Query(default=None)
    katottg_code: str | None = Query(default=None)
    katottg_name: str | None = Query(default=None)
    katottg_category: KATOTTGCategory | None = Query(default=None)


class GetKATOTTGListResponse(ListResponseBase):
    results: list[KATOTTG]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": docs.GET_KATOTTG_LIST_RESPONSE_EXAMPLE,
        }


class GetKATOTTGListLegacyResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[KATOTTG]


class GetKOATUUListResponse(ListResponseBase):
    results: list[KOATUU]

    class Config:
        orm_mode = True
