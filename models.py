from pydantic import BaseModel


class Text(BaseModel):
    text: str
    color: str
    pos: str
    size: int
    center: bool
