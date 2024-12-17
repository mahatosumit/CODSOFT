# app.py
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def minimax(board, depth, is_maximizing, alpha, beta):
    scores = {'X': -10, 'O': 10, 'tie': 0}
    winner = check_winner(board)
    if winner:
        return scores[winner]
    
    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ''
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ''
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
            
    if '' not in board:
        return 'tie'
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    board = request.json['board']
    
    # Find best AI move
    best_score = float('-inf')
    best_move = None
    
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, 0, False, float('-inf'), float('inf'))
            board[i] = ''
            if score > best_score:
                best_score = score
                best_move = i
    
    board[best_move] = 'O'
    winner = check_winner(board)
    
    return jsonify({
        'move': best_move,
        'winner': winner,
        'board': board
    })

if __name__ == '__main__':
    app.run(debug=True)