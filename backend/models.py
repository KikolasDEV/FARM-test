from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import Optional, Any
from bson import ObjectId


class PyObjectId:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)


class Task(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True
        populate_by_name = True
        json_enconders = {ObjectId: str}
