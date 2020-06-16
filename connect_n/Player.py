import abc


class Player(abc.ABC):
    @abc.abstractmethod
    def move(self, board, possible_moves):
        pass
