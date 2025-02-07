class Game:
    def __init__(self, players: str="OX") -> None:
        board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.current_index = 0
        self.current_player = players[self.current_index]

class Com:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
   game = Game()
    while True:
        game.action(input(f"{game.current_player}"))
    
