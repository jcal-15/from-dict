from dataclasses import dataclass
from typing import Any, Optional, Union, TypeVar, Generic, Literal

import attr

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
# Classes used by the tests

class NormalClass:
    def __init__(self, v: str) -> None:
        self.value = v

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NormalClass) and self.value == other.value


@dataclass(frozen=True)
class DataClass:
    field: str


@attr.s(auto_attribs=True)
class AttrClass:
    attrib: str


T = TypeVar("T")
@dataclass
class GenericDataClass(Generic[T]):
    field: T

@dataclass
class GenericDataClassSubClass(GenericDataClass[str]):
    another: int

TTestType = TypeVar("TTestType")
TSelfRef = TypeVar("TSelfRef")

@dataclass
class ClassBase(Generic[TTestType, TSelfRef]):
    normal: TTestType
    optional: Optional[TTestType]
    union: Union[str, NormalClass, DataClass, TTestType]
    any: Any
    self_ref: Optional[TSelfRef]

    list_normal: list[TTestType]
    list_optional: list[Optional[TTestType]]
    list_union: list[Union[str, NormalClass, DataClass, TTestType]]
    list_any: list[Any]
    list_self_ref: list[TSelfRef]
    
    dict_normal: dict[str, TTestType]
    dict_optional: dict[str, Optional[TTestType]]
    dict_union: dict[str, Union[str, NormalClass, DataClass, TTestType]]
    dict_any: dict[str, Any]
    dict_self_ref: dict[str, TSelfRef]


ClassPrimitives = ClassBase[int, "ClassPrimitives"]
ClassDict = ClassBase[dict[str,str], "ClassDict"]
ClassDictSimple = ClassBase[dict, "ClassDictSimple"]
ClassList = ClassBase[list[str], "ClassList"]
ClassDataClass = ClassBase[DataClass, "ClassDataClass"]
ClassNormalClass = ClassBase[NormalClass, "ClassNormalClass"]
ClassAttrClass = ClassBase[AttrClass, "ClassAttrClass"]
ClassListDataClass = ClassBase[list[DataClass], "ClassListDataClass"]
ClassDictDataClass = ClassBase[dict[str, DataClass], "ClassDictDataClass"]
ClassLiteral = ClassBase[Literal["my-literal"], "ClassLiteral"]
ClassMultiLiteral = ClassBase[Literal[2, 3, 5, 7, 11], "ClassMultiLiteral"]

ClassGenericDataClassINT = ClassBase[GenericDataClass[int], "ClassGenericDataClassINT"]
ClassGenericDataClassSubClass = ClassBase[GenericDataClassSubClass, "ClassGenericDataClassSubClass"]