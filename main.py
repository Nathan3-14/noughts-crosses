import os
import random
from typing import List


def list_replace(_list: List[str], value: str, replace: str) -> List[str]:
    return [replace if current == value else current for current in _list]

WIN_STATE = 0
TIE_STATE = 1
CONTINUE_STATE = 2

class Game:
    def __init__(self, players: str="OX") -> None:
        self.players = players
        self.board_reference = [
            ["0", "1", "2"],
            ["3", "4", "5"],
            ["6", "7", "8"]
        ]
        self.board_current = self.board_reference.copy()
        self.current_index = 0
        self.current_player = players[self.current_index]
    
    def get_board(self, index: str) -> str:
        for layer_index, layer in enumerate(self.board_reference):
            if index not in layer:
                continue
            return self.board_current[layer_index][layer.index(index)]
        return "@"
        
    def set_board(self, index: str) -> None:
        for layer_index, layer in enumerate(self.board_reference):
            if index not in layer:
                continue
            self.board_current[layer_index] = list_replace(self.board_current[layer_index], index, self.current_player)
    
    def get_boardstate(self) -> str:
        return "".join(["".join(layer) for layer in self.board_current])
    
    def get_board_display(self, start: str="\n\n\n") -> str:
        return start + "\n-+-+-\n".join([f"{layer[0]}|{layer[1]}|{layer[2]}" for layer in self.board_current])
    
    def action(self, location: str) -> str:
        self.set_board(location)
        checkwin_state = self.check_win()
        if checkwin_state == WIN_STATE:
            return self.current_player
        elif checkwin_state == TIE_STATE:
            return "##tie##"
        
        self.current_index += 1
        if self.current_index >= len(self.players):
            self.current_index -= len(self.players)
        self.current_player = self.players[self.current_index]
        return ""
    
    def check_win(self) -> int:
        first_pos = self.get_board("0")
        for pos in range(1, 9):
            if self.get_board(str(pos)) != first_pos:
                break
        else:
            return TIE_STATE
        
        conditions = [
            "012", "345", "678",
            "036", "147", "258",
            "048", "246"
        ]
        for condition in conditions:
            print(f"Getting {condition[0]}, {condition[1]}, {condition[2]}")
            if self.get_board(condition[0]) == self.get_board(condition[1]) == self.get_board(condition[2]):
                return WIN_STATE
        return CONTINUE_STATE
            

class Com:
    def __init__(self, path: str) -> None:
        self.data_path = os.path.join(os.getcwd(), path)
        self.choice_path = []
    
    def get_action(self, board_state: str, players: str="OX") -> str:
        board_state_path = os.path.join(self.data_path, f"{board_state}.txt")
        if not os.path.exists(board_state_path):
            to_write = ""
            for char in board_state:
                if char not in players:
                    to_write += char
            open(board_state_path, "w").write(to_write)
        data = open(board_state_path, "r").read()
        choice = random.choice(data)
        self.choice_path.append(choice)
        return choice

    def reward(self) -> None:
        pass
    def maintain(self) -> None:
        pass
    def punish(self) -> None:
        pass
            

if __name__ == "__main__":    
    # print(list_replace(["0", "1", "2"], "0", "3"))
    game = Game()
    com = Com("./data")
    while True:
        print(game.get_board_display())
        result = game.action(input(f"Current Player: {game.current_player}\n  "))
        if result != "":
            print(f"\n\n\n\n{result} has won!")
            print(game.get_board_display(start=""))
            quit()
        result = game.action(com.get_action(game.get_boardstate()))
        if result != "":
            print(f"\n\n\n\n{result} has won!")
            print(game.get_board_display(start=""))
            quit()
        print(game.get_boardstate())
    
