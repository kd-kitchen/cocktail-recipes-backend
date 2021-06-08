from dataclasses import dataclass

__all__ = ['Account']


@dataclass
class Account:
    id: int
    username: str
    password: str
    email: str
    is_admin: bool

    def to_dict(self):
        return vars(self)
