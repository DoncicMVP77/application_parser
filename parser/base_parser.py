from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def get_category_shop_response(self):
        pass

    @abstractmethod
    def get_category_products_list_response(self):
        pass

    @abstractmethod
    def get_shop_information_response(self):
        pass

    @abstractmethod
    def get_city_shop_response(self):
        pass

    @abstractmethod
    def parse_category_shop_response(self, data):
        pass

    @abstractmethod
    def parse_city_shop_response(self, data):
        pass

    @abstractmethod
    def get_dict_with_category_shop(self) -> dict:
        pass
