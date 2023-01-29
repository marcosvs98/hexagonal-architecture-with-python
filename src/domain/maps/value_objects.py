import re
from enum import Enum
from typing import TYPE_CHECKING
from domain.base.value_object import ValueObject
from domain.base.model import Attribute, AttributeSetter

from typing import Union, TYPE_CHECKING
from domain.base.primitive_value_object import PrimitiveValueObject


class AddressEntry(PrimitiveValueObject[str]):
    value_type = str

    if TYPE_CHECKING:
        def __init__(self, value: Union[str, 'AddressEntry']):
            super().__init__(...)


class DistanceKm(PrimitiveValueObject[float]):
    value_type = float

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if value < 0:
            raise ValueError(f'Expected DistanceKm >= 0, got {value}')

        return value

    if TYPE_CHECKING:
        def __init__(self, value: Union[float, 'DistanceKm']):
            super().__init__(value)


class Postcode(PrimitiveValueObject[str]):
    value_type = str

    @classmethod
    def _validate(cls, value):
        value = super()._validate(value)

        if not re.match(r'^\d{5}$', value):
            raise ValueError(f'Postcode must be a string of 5 digits, got {value}')

        return value

    if TYPE_CHECKING:
        def __init__(self, postcode: Union[str, 'Postcode']):
            super().__init__(...)


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


class Province(PrimitiveValueObject[str]):
    value_type = str
    Enum = ProvinceEnum

    def bangkok_and_surrounding(self) -> bool:
        return self._value in _bangkok_and_surrounding_provinces

    @classmethod
    def _validate(cls, value):
        if isinstance(value, ProvinceEnum):
            value = value.value
        value = super()._validate(value)

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
    house_number: AddressEntry = Attribute()
    road: AddressEntry = Attribute()
    sub_district: AddressEntry = Attribute()
    district: AddressEntry = Attribute()
    province: Province = Attribute()
    postcode: Postcode = Attribute()
    country: AddressEntry = Attribute()

    @classmethod
    def build(cls, house_number: str, road: str, sub_district: str, district: str, province: str,
              postcode: str, country: str):
        return cls(house_number=AddressEntry(house_number), road=AddressEntry(road),
                   sub_district=AddressEntry(sub_district), district=AddressEntry(district),
                   province=Province(province), postcode=Postcode(postcode), country=AddressEntry(country))

    def bangkok_and_surrounding(self) -> bool:
        return self._province.bangkok_and_surrounding()

    if TYPE_CHECKING:
        def __init__(self, house_number: AddressEntry, road: AddressEntry, sub_district: AddressEntry,
                     district: AddressEntry, province: Province, postcode: Postcode, country: AddressEntry):
            super().__init__()

    _house_number: AddressEntry = AttributeSetter()
    _road: AddressEntry = AttributeSetter()
    _sub_district: AddressEntry = AttributeSetter()
    _district: AddressEntry = AttributeSetter()
    _province: Province = AttributeSetter()
    _postcode: Postcode = AttributeSetter()
    _country: AddressEntry = AttributeSetter()

