import random

class MarkovRPS:
    def __init__(self):
        # Track transitions: {previous_move: {next_move: count}}
        self.transitions = {'R': {'R':0, 'P':0, 'S':0},
                            'P': {'R':0, 'P':0, 'S':0},
                            'S': {'R':0, 'P':0, 'S':0}}
        self.last_move = None

    def predict_next_move(self):
        if self.last_move is None:
            # No data, pick random
            return random.choice(['R','P','S'])
        next_moves = self.transitions[self.last_move]
        # Pick most probable next move
        predicted_move = max(next_moves, key=next_moves.get)
        return predicted_move

    def update_transitions(self, current_move):
        if self.last_move is not None:
            self.transitions[self.last_move][current_move] += 1
        self.last_move = current_move

    def choose_move(self):
        predicted = self.predict_next_move()
        # To beat predicted move
        beats = {'R':'P', 'P':'S', 'S':'R'}
        return beats[predicted]

def play():
    ai = MarkovRPS()
    print("Rock-Paper-Scissors with Markov AI! Enter R, P or S. Type Q to quit.")
    while True:
        player_move = input("Your move: ").upper()
        if player_move == 'Q':
            break
        if player_move not in ['R','P','S']:
            print("Invalid input.")
            continue
        ai_move = ai.choose_move()
        print(f"AI move: {ai_move}")
        if ai_move == player_move:
            print("Draw!")
        elif (player_move == 'R' and ai_move == 'S') or \
             (player_move == 'P' and ai_move == 'R') or \
             (player_move == 'S' and ai_move == 'P'):
            print("You win!")
        else:
            print("AI wins!")
        ai.update_transitions(player_move)

if __name__ == "__main__":
    play()
