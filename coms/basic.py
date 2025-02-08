import random, os
from typing import List, Tuple

class BasicCom:
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

            choice_data = choice_data.replace(choice_decision, "", 1)

            open(choice_filepath, "w").write(choice_data)