import datetime
from dataclasses import dataclass

__all__ = ['Ingredient']


@dataclass
class Ingredient:
    iid: int
    name: str
    creator_id: str
    creation_date: datetime.datetime
    last_updated: datetime.datetime
    description: str
    # tags: []

    def to_dict(self):
        return vars(self)
