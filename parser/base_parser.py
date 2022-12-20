from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def parse_category_site(self, body: str) -> None:
        pass

    @abstractmethod
    def get_category_site(self):
        pass
