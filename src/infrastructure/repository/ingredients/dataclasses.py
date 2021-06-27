from dataclasses import dataclass

__all__ = ['Ingredient']


@dataclass
class Ingredient:
    id: int
    name: str
    description: str
    # tags: []

    def to_dict(self):
        return vars(self)
