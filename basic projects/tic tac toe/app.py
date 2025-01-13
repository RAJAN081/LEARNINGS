from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Initialize scores
scores = {"Player": 0, "AI": 0}
board = [""] * 9  # Empty Tic Tac Toe board

@app.route('/')
def index():
    # Render the main HTML page
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    global board
    board = [""] * 9  # Reset board
    player_name = request.json.get("player_name", "Player")
    return jsonify({"scores": scores})

@app.route('/play', methods=['POST'])
def play_move():
    global board
    move = request.json.get("move")
    
    # If the spot is already taken, return the current state
    if board[move] != "":
        return jsonify({"board": board, "scores": scores})
    
    board[move] = "X"  # Player's move

    # Check for a winner
    winner = check_winner(board)
    if winner:
        scores[winner] += 1
        return jsonify({"board": board, "winner": winner, "scores": scores})

    # AI move (just a random empty spot for simplicity)
    ai_move = random.choice([i for i, x in enumerate(board) if x == ""])
    board[ai_move] = "O"  # AI's move

    # Check for a winner again
    winner = check_winner(board)
    if winner:
        scores[winner] += 1
        return jsonify({"board": board, "winner": winner, "scores": scores})

    return jsonify({"board": board, "winner": None, "scores": scores})

def check_winner(board):
    # Winning combinations
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return "Player" if board[combo[0]] == "X" else "AI"
    return None

if __name__ == '__main__':
    app.run(debug=True)

