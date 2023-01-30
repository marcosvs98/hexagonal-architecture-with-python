import re
from enum import Enum
from typing import TYPE_CHECKING
from domain.base.value_object import ValueObject
from typing import Union, TYPE_CHECKING
from pydantic import validator


class ProvinceEnum(str, Enum):
    BANGKOK: str = 'bangkok'
    NAKHON_PATHOM: str = 'nakhon pathom'
    NONTHABURI: str = 'nonthaburi'
    PATHUM_THANI: str = 'pathum thani'
    SAMUT_PRAKAN: str = 'samut prakan'
    SAMUT_SAKHON: str = 'samut sakhon'
    CHIANG_MAI: str = 'chiang mai'

    @classmethod
    def has_value(cls, value):
        return value in cls._member_map_.values()


class Province(ValueObject):
    enum: str = ProvinceEnum

    def bangkok_and_surrounding(self) -> bool:
        return self.value in _bangkok_and_surrounding_provinces

    @validator('enum', check_fields=False)
    def validate(cls, value):
        if not ProvinceEnum.has_value(value):
            raise ValueError(f'Province named "{value}" not exists')
        return value

    if TYPE_CHECKING:
        def __init__(self, value: Union[str, 'Province']):
            super().__init__(...)


_bangkok_and_surrounding_provinces = {
    ProvinceEnum.BANGKOK,
    ProvinceEnum.NAKHON_PATHOM,
    ProvinceEnum.NONTHABURI,
    ProvinceEnum.PATHUM_THANI,
    ProvinceEnum.SAMUT_PRAKAN,
    ProvinceEnum.SAMUT_SAKHON,
}

class Address(ValueObject):
    house_number: str#AddressEntry# = Attribute()
    road: str#AddressEntry# = Attribute()
    sub_district: str#AddressEntry# = Attribute()
    district: str#AddressEntry# = Attribute()
    province: str#Province# = Attribute()
    postcode: str#Postcode# = Attribute()
    country: str#AddressEntry# = Attribute()

    @classmethod
    def build(cls, house_number: str, road: str, sub_district: str, district: str, province: str,
              postcode: str, country: str):
        return cls(house_number=house_number, road=road,
                   sub_district=sub_district, district=district,
                   province=province, postcode=postcode, country=country)

    def bangkok_and_surrounding(self) -> bool:
        return self.province.bangkok_and_surrounding()

