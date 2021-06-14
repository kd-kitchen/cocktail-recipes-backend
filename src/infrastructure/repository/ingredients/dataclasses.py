import datetime
from dataclasses import dataclass

__all__ = ['Ingredient']


@dataclass
class Ingredient:
    iid: int
    iname: str
    creator_id: int
    creation_date: str
    last_updated: datetime.datetime
    description: str
    # tags: []

    def to_dict(self):
        return vars(self)
