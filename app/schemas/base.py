from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda d: d.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        },
        "alias_generator": lambda field_name: field_name,
        "from_attributes": True,
    }
