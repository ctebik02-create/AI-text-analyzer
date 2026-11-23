from pydantic import BaseModel, ConfigDict
from pydantic.types import StringConstraints
from typing import Literal, Annotated
from datetime import datetime

class ClientInput(BaseModel):
    text: Annotated[str, StringConstraints(
        strip_whitespace=True,
        min_length=1
    )]


class AIOutput(BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]

class Output(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    input_text: str
    sentiment: Literal["positive", "negative", "neutral"]
    summary: str
    created_at: datetime
