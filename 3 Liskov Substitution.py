from dataclasses import dataclass
from typing import Protocol

class RectangleLike(Protocol):
    def area(self) -> int:
        ...
    def with_width(self, v: int) -> 'RectangleLike':
        ...
    def with_height(self, v: int) -> 'RectangleLike':
        ...

@dataclass(frozen=True)
class Rectangle:
    width: int
    height: int
    
    def area(self) -> int:
        return self.width * self.height
    
    def with_width(self, v: int) -> 'Rectangle':
        return Rectangle(v, self.height)
    
    def with_height(self, v: int) -> 'Rectangle':
        return Rectangle(self.width, v)

@dataclass(frozen=True)
class Square:
    side: int
    
    def area(self) -> int:
        return self.side * self.side
    
    def with_width(self, v: int) -> 'Square':
        return Square(v)
    
    def with_height(self, v: int) -> 'Square':
        return Square(v)

def resize_and_get_area(r: RectangleLike) -> int:
    r2 = r.with_width(10).with_height(5)
    return r2.area()