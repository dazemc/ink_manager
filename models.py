from pydantic import BaseModel


class Text(BaseModel):
    text: str
    color: str
    pos: str
    size: int
    center: bool


class QuoteLine(BaseModel):
    boundary_x: int
    boundary_y: int
    text: str


class Quote(BaseModel):
    origin_coord: tuple[int, int]
    quote_lines: list[QuoteLine]
    boundary_x: int
    boundary_y: int
