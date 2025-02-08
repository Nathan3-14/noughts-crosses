from re import match

class PatternCom:
    def __init__(self) -> None:
        self.hmatch = r"(?:^|...)(OO.)|(O.O)|(.OO)(?:(...)|$)"
        self.vmatch = r"O..O..O"
        self.dmatch = r"(O...O...O)|(..O.O.O..)"
    
    def get_action(self, boardstate: str, players: str="OX") -> str:
        hmatched = match(self.hmatch, boardstate)
        if hmatched:
            print(hmatched.group())
        
        return "1"
        