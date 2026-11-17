from pydantic import BaseModel
from typing import Literal

class ClientInput(BaseModel):
    text: str


class AIOutput(BaseModel):
    summary: str
    sentiment: Literal["positive", "negative", "neutral"]

