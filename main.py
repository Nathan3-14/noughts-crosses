import os
from typing import Dict, List
from random import choice

class Game:
    def __init__(self) -> None:
        self.board: List[str] = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
        self.prior_actions: Dict[str, int] = {}
    
    def get_action(self) -> None:
        path = f"data/{"".join(self.board)}.txt"
        if not os.path.exists(path):
            for index, item in enumerate(self.board):
                print(f"{index}: '{item}'")
            open(path, "w").write("".join([str(index) for index, item in enumerate(self.board) if item == "_"]*5))
        possible = [int(num) for num in open(path, "r").read()]
        decision = choice(possible)
        self.prior_actions["".join(self.board)] = decision
        self.board[decision] = "X"
    
    def set_player(self, position: int) -> bool:
        if self.board[position] != "_":
            return False
        self.board[position] = "O"
        return True

    def punish(self) -> None:
        ...
    
    def reward(self) -> None:
        ...
    
    def play(self) -> None:
        self.display_board()
        has_been_set = False
        while not has_been_set:
            has_been_set = self.set_player(int(input("Action (0-8) ")))
    
    def display_board(self) -> None:
        print(f"{self.board[0]}|{self.board[1]}|{self.board[2]}")
        print("-+-+-")
        print(f"{self.board[3]}|{self.board[4]}|{self.board[5]}")
        print("-+-+-")
        print(f"{self.board[6]}|{self.board[7]}|{self.board[8]}")

if __name__ == "__main__":
    game = Game()
    while True:
        game.play()
        game.get_action()

