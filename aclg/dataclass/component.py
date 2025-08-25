# component.py
from dataclasses import dataclass

@dataclass
class Component:
    """
    (x, y) center of the component
    (width, height) size of the component
    level: hierarchy level of the component
    relation_id: the unique identifier for the component's relation to others
    generate_rule: the rule used to generate the component
    """
    x: float
    y: float
    width: float
    height: float
    level: int = 0
    relation_id: int = 0
    generate_rule: str = ""
    sub_components: list["Component"] = None

    def get_topleft(self):
        return (self.x - self.width / 2, self.y - self.height / 2)
    def get_bottomright(self):
        return (self.x + self.width / 2, self.y + self.height / 2)