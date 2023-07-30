from abc import ABC, abstractmethod


class ParserAPI(ABC):

    @abstractmethod
    def get_request(self):
        raise NotImplementedError("В дочернем классе должен быть переопределен метод get_request()")
