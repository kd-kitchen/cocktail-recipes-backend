from fastapi import Depends

from src.dependencies.session import Session, get_session

__all__ = ['BaseRepo']


class BaseRepo:
    def __init__(self, session=Depends(get_session)):
        self.session: Session = session
