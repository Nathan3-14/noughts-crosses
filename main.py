from typing import List

from coms import BasicCom, PatternCom


def list_replace(_list: List[str], value: str, replace: str) -> List[str]:
    return [replace if current == value else current for current in _list]

WIN_STATE = 0
TIE_STATE = 1
CONTINUE_STATE = 2

class Game:
    def __init__(self, players: str="OX") -> None:
        self.players = players
        self.board_state = "012345678"
        
        # self.board_reference = [
        #     ["0", "1", "2"],
        #     ["3", "4", "5"],
        #     ["6", "7", "8"]
        # ]
        # self.board_current = self.board_reference.copy()
        self.current_index = 0
        self.current_player = players[self.current_index]
    
    def get_board(self, index: str|int) -> str:
        lookup_index = (int(index) // 3) + (int(index) - 1 % 3)
        return self.board_state[lookup_index]
        return "@"
        
    def set_board(self, index: str) -> bool:
        lookup_index = ((int(index) // 3 ) * 3) + (int(index) % 3)
        did_get_set = False
        for char_index, char in enumerate(self.board_state):
            if char_index == lookup_index:
                self.board_state = self.board_state[:char_index] + self.current_player + self.board_state[char_index+1:]
                did_get_set = True
                break
        return not did_get_set
    
    def get_boardstate(self) -> str:
        return self.board_state
    
    def get_board_display(self, start: str="\n\n\n") -> str:
        board_display = ""
        for index, char in enumerate(self.board_state):
            board_display += char
            if (index + 1) / 3 in [1, 2]:
                board_display += "\n-+-+-\n"
            elif index != 8:
                board_display += "|"
            
        return start + board_display
    
    def action(self, location: str) -> str:
        if self.set_board(location):
            print(f"invalid position {location}")
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
             
                      
def display_results(result: str) -> None:
        print(f"\n\n\n\n{result} has won!" if result != "##tie##" else "It's a tie!")
        print(game.get_board_display(start=""))
        quit()

def basiccom(game: Game) -> None:
    com = BasicCom("./coolmath")
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

def patterncom(game: Game) -> None:
    com = PatternCom()
    while True:
        print(game.get_board_display())
        
        #* Player Actions *#
        result = "##invalid##"
        while result == "##invalid##":
            result = game.action(input(f"Current Player: {game.current_player}\n>> "))
        if result != "":
            match result:
                case "##tie##":
                    pass
                case "O": #O is always the player
                    pass
                #Com cannot win on player's turn
            display_results(result)
        
        #* Com Actions *#
        result = game.action(com.get_action(game.get_boardstate()))
        if result != "":
            match result:
                case "##tie##":
                    pass
                case "X": #X is always the com
                    pass
                #Player cannont win on com's turn
            display_results(result)
    

if __name__ == "__main__":   
    game = Game()
    game.get_board(5)
    # basiccom(game)
    patterncom(game)
