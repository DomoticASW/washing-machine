from dataclasses import dataclass
from enum import Enum
from typing import Union, Optional, List, Set, NewType

from pydantic import BaseModel

ActionId = NewType("ActionId", str)
PropertyId = NewType("PropertyId", str)

class Color(BaseModel):
    r: int
    g: int
    b: int

ActualTypes = Union[str, int, float, bool, Color, None]

class Type(str, Enum):
    STRING = "String"
    BOOLEAN = "Boolean"
    INT = "Int"
    DOUBLE = "Double"
    COLOR = "Color"
    VOID = "Void"

class TypeConstraintEnum(BaseModel):
    values: List[str]

class TypeConstraintIntRange(BaseModel):
    min: int
    max: int

class TypeConstraintDoubleRange(BaseModel):
    min: float
    max: float

class TypeConstraintNone(BaseModel):
    type: Type

TypeConstraints = Union[
    TypeConstraintEnum,
    TypeConstraintIntRange,
    TypeConstraintDoubleRange,
    TypeConstraintNone,
]

class DeviceProperty(BaseModel):
    id: PropertyId
    name: str
    value: ActualTypes

class DevicePropertyWithSetter(DeviceProperty):
    setterActionId: ActionId

class DevicePropertyWithTypeConstraint(DeviceProperty):
    typeConstraints: TypeConstraints

class DeviceAction(BaseModel):
    id: ActionId
    name: str
    description: Optional[str]
    inputTypeConstraints: TypeConstraints

class DeviceRegistration(BaseModel):
    id: str
    name: str
    properties: List[DevicePropertyWithSetter | DevicePropertyWithTypeConstraint]
    actions: List[DeviceAction]
    events: List[str]