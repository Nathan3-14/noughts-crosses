import os
import random
from typing import List, Tuple


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
        
    def set_board(self, index: str) -> bool:
        did_get_set = False
        for layer_index, layer in enumerate(self.board_current):
            if index not in layer:
                continue
            self.board_current[layer_index] = list_replace(self.board_current[layer_index], index, self.current_player)
            did_get_set = True
        return not did_get_set
    
    def get_boardstate(self) -> str:
        return "".join(["".join(layer) for layer in self.board_current])
    
    def get_board_display(self, start: str="\n\n\n") -> str:
        return start + "\n-+-+-\n".join([f"{layer[0]}|{layer[1]}|{layer[2]}" for layer in self.board_current])
    
    def action(self, location: str) -> str:
        if self.set_board(location):
            return "##invalid##"
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
        
        conditions = [
            "012", "345", "678",
            "036", "147", "258",
            "048", "246"
        ]
        for condition in conditions:
            print(f"Getting {condition[0]}, {condition[1]}, {condition[2]}")
            if self.get_board(condition[0]) == self.get_board(condition[1]) == self.get_board(condition[2]):
                return WIN_STATE
        
        for pos in range(1, 9):
            if self.get_board(str(pos)) not in ["X", "O"]:
                break
        else:
            return TIE_STATE

        return CONTINUE_STATE
            

class Com:
    def __init__(self, path: str) -> None:
        self.data_path = os.path.join(os.getcwd(), path)
        self.choice_path: List[Tuple[str, str]] = []
    
    def get_action(self, board_state: str, players: str="OX") -> str:
        board_state_path = os.path.join(self.data_path, f"{board_state}.txt")
        if not os.path.exists(board_state_path):
            to_write = ""
            for char in board_state:
                if char not in players:
                    to_write += char
                    to_write += char
                    to_write += char
                    to_write += char
                    to_write += char
            open(board_state_path, "w").write(to_write)
        data = open(board_state_path, "r").read()
        choice = random.choice(data)
        self.choice_path.append((board_state_path, choice))
        return choice

    def reward(self) -> None:
        for choice_tuple in self.choice_path:
            choice_filepath = choice_tuple[0]
            choice_decision = choice_tuple[1] 
            choice_data = open(choice_filepath, "r").read()

            choice_data += choice_decision
            choice_data += choice_decision
            choice_data += choice_decision

            open(choice_filepath, "w").write(choice_data)
    def maintain(self) -> None:
        for choice_tuple in self.choice_path:
            choice_filepath = choice_tuple[0]
            choice_decision = choice_tuple[1] 
            choice_data = open(choice_filepath, "r").read()

            choice_data += choice_decision

            open(choice_filepath, "w").write(choice_data)
    def punish(self) -> None:
        print(self.choice_path)
        for choice_tuple in self.choice_path:
            choice_filepath = choice_tuple[0]
            choice_decision = choice_tuple[1] 
            choice_data = open(choice_filepath, "r").read()

            choice_data = choice_data.replace(choice_decision, "", count=1)

            open(choice_filepath, "w").write(choice_data)
            

if __name__ == "__main__":
    def display_results(result: str) -> None:
            print(f"\n\n\n\n{result} has won!" if result != "##tie##" else "It's a tie!")
            print(game.get_board_display(start=""))
            quit()
       
    game = Game()
    com = Com("./coolmath")
    while True:
        print(game.get_board_display())
        
        #* Player Actions *#
        result = "##invalid##"
        while result == "##invalid##":
            result = game.action(input(f"Current Player: {game.current_player}\n  "))
        if result != "":
            match result:
                case "##tie##":
                    com.maintain()
                case "O": #O is always the player
                    com.punish()    
                #Com cannot win on player's turn
            display_results(result)
        
        #* Com Actions *#
        result = game.action(com.get_action(game.get_boardstate()))
        if result != "":
            match result:
                case "##tie##":
                    com.maintain()
                case "X": #X is always the com
                    com.reward()
                #Player cannont win on com's turn
            display_results(result)
