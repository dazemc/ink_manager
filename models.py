from pydantic import BaseModel


class Coord(BaseModel):
    x: int
    y: int


class Text(BaseModel):
    text: str
    color: str
    pos: str
    size: int
    center: bool


class TextBoundaryLine(BaseModel):
    boundary_x: int
    boundary_y: int
    text: str


class TextBoundary(BaseModel):
    origin_coord: Coord
    text_lines: list[TextBoundaryLine]
    boundary_x: int
    boundary_y: int
    max_line_height: int
