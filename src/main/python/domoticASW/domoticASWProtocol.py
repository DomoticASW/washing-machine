from dataclasses import dataclass
from enum import Enum
from typing import Union, Optional, List, Set, NewType

ActionId = NewType("ActionId", str)
PropertyId = NewType("PropertyId", str)

@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int

ActualTypes = Union[str, int, float, bool, Color, None]

class Type(Enum):
    STRING = "String"
    BOOLEAN = "Boolean"
    INT = "Int"
    DOUBLE = "Double"
    COLOR = "Color"
    VOID = "Void"

@dataclass(frozen=True)
class TypeConstraintEnum:
    values: Set[str]

@dataclass(frozen=True)
class TypeConstraintIntRange:
    min: int
    max: int

@dataclass(frozen=True)
class TypeConstraintDoubleRange:
    min: float
    max: float

@dataclass(frozen=True)
class TypeConstraintNone:
    type: Type

TypeConstraints = Union[
    TypeConstraintEnum,
    TypeConstraintIntRange,
    TypeConstraintDoubleRange,
    TypeConstraintNone,
]

@dataclass(frozen=True)
class DeviceProperty:
    id: PropertyId
    name: str
    value: ActualTypes

@dataclass(frozen=True)
class DevicePropertyWithSetter(DeviceProperty):
    setterActionId: ActionId

@dataclass(frozen=True)
class DevicePropertyWithTypeConstraint(DeviceProperty):
    typeConstraints: TypeConstraints

@dataclass(frozen=True)
class DeviceAction:
    id: ActionId
    name: str
    description: Optional[str]
    inputTypeConstraints: TypeConstraints

@dataclass(frozen=True)
class DeviceRegistration:
    id: str
    name: str
    properties: List[DeviceProperty]
    actions: List[DeviceAction]
    events: List[str]