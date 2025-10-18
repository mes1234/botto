from abc import ABC, abstractmethod
from typing import Self


class BottoMessage(ABC):
    """
    Base class for all messages in Botto framework."""

    @classmethod
    @abstractmethod
    def from_dict(cls, d: dict) -> Self:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
