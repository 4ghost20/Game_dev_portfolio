# tictactoe_minimax.py
# Human is 'X' (goes first). AI is 'O' (minimax, perfect play).

from typing import List, Optional, Tuple

Board = List[List[str]]

class TicTacToe:
    def __init__(self):
        self.board: Board = [[" " for _ in range(3)] for _ in range(3)]

    # ---------- Board helpers ----------
    def print_board(self) -> None:
        rows = []
        for r in range(3):
            rows.append(" | ".join(self.board[r]))
        sep = "\n" + "-" * 9 + "\n"
        print("\n" + sep.join(rows) + "\n")

    def reset(self) -> None:
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def possible_moves(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

    def make_move(self, r: int, c: int, player: str) -> bool:
        if 0 <= r < 3 and 0 <= c < 3 and self.board[r][c] == " ":
            self.board[r][c] = player
            return True
        return False

    def undo_move(self, r: int, c: int) -> None:
        self.board[r][c] = " "

    # ---------- Win/draw detection ----------
    def check_winner(self) -> Optional[str]:
        b = self.board
        # rows
        for r in range(3):
            if b[r][0] != " " and b[r][0] == b[r][1] == b[r][2]:
                return b[r][0]
        # cols
        for c in range(3):
            if b[0][c] != " " and b[0][c] == b[1][c] == b[2][c]:
                return b[0][c]
        # diagonals
        if b[0][0] != " " and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] != " " and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]
        return None

    def is_draw(self) -> bool:
        return self.check_winner() is None and all(self.board[r][c] != " " for r in range(3) for c in range(3))

    # ---------- Minimax ----------
    # We evaluate from AI ('O') perspective:
    #   AI win  -> +1
    #   Draw    ->  0
    #   AI lose -> -1
    #
    # Depth is used to slightly prefer faster wins (and delay losses):
    #   win score becomes  1 * (1 + 0.05*(9 - depth))
    #   loss score becomes -1 * (1 + 0.05*(9 - depth))
    def minimax(self, depth: int, is_maximizing: bool) -> float:
        winner = self.check_winner()
        if winner == "O":
            return 1.0 + 0.05 * (9 - depth)
        if winner == "X":
            return -1.0 - 0.05 * (9 - depth)
        if self.is_draw():
            return 0.0

        if is_maximizing:  # AI's turn ('O')
            best_score = float("-inf")
            for (r, c) in self.possible_moves():
                self.make_move(r, c, "O")
                score = self.minimax(depth + 1, False)
                self.undo_move(r, c)
                if score > best_score:
                    best_score = score
            return best_score
        else:  # Human's turn ('X'), minimize AI's score
            best_score = float("inf")
            for (r, c) in self.possible_moves():
                self.make_move(r, c, "X")
                score = self.minimax(depth + 1, True)
                self.undo_move(r, c)
                if score < best_score:
                    best_score = score
            return best_score

    def best_ai_move(self) -> Tuple[int, int]:
        best_score = float("-inf")
        best_move = (-1, -1)
        for (r, c) in self.possible_moves():
            self.make_move(r, c, "O")
            score = self.minimax(depth=0, is_maximizing=False)  # after AI move, it's human's turn
            self.undo_move(r, c)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_move

# ---------- CLI Game ----------
def to_rc(choice: int) -> Tuple[int, int]:
    """Map keypad-style 1..9 to (row, col):
       1 2 3
       4 5 6
       7 8 9
    """
    choice -= 1
    return (choice // 3, choice % 3)

def play():
    game = TicTacToe()
    print("Tic-Tac-Toe — You are X (first). AI is O.")
    print("Choose positions 1..9 as:\n 1 2 3\n 4 5 6\n 7 8 9\n")
    game.print_board()

    while True:
        # Human turn
        while True:
            raw = input("Your move (1-9) or Q to quit: ").strip().upper()
            if raw == "Q":
                print("Bye!")
                return
            if not raw.isdigit():
                print("Enter a number 1-9.")
                continue
            n = int(raw)
            if n < 1 or n > 9:
                print("Enter a number 1-9.")
                continue
            r, c = to_rc(n)
            if game.make_move(r, c, "X"):
                break
            else:
                print("That cell is taken. Try another.")

        game.print_board()
        if game.check_winner() == "X":
            print("You win! 🎉")
            return
        if game.is_draw():
            print("Draw!")
            return

        # AI turn
        r, c = game.best_ai_move()
        game.make_move(r, c, "O")
        print(f"AI plays at {r*3 + c + 1}")
        game.print_board()

        if game.check_winner() == "O":
            print("AI wins! 🤖")
            return
        if game.is_draw():
            print("Draw!")
            return

if __name__ == "__main__":
    play()
