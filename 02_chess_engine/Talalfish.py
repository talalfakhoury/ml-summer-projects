import chess

# this is me trnying to understand the chess library and how to use it to build a chess engine

# board = chess.Board() 

#print(board)

# understanding the board and making moves
# board.push_san("e4")
# print(board)
# board.pop()
# print(board)
# print(board.is_checkmate())
#building stockfish chess engine using python-chess library


# # loop to have both players make moves until the game is over
# while not board.is_game_over():
#     current_player = "White" if board.turn == chess.WHITE else "Black"
#     print(f"{current_player}'s turn. Legal moves: {board.legal_moves}")
#     move = input("Enter your move in UCI format (e.g., e2e4): ")
#     try:
#         board.push_san(move)
#         print(board)
#     except ValueError:
#         print("Invalid move. Please try again.")
#     else:
#         print("Invalid move. Please try again.")    

def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    else:
        return 0
    

# evaluate the board function 

def evaluate_board(board):
    evaluation = 0 
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = piece_value(piece)
            if piece.color == chess.WHITE:
                evaluation += value
            else:
                evaluation -= value 

    return evaluation



# building the model: 

def minimax(board, depth):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    # if white is playing, we want to maximize the evaluation
    if board.turn == chess.WHITE:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    # if black is playing, we want to minimize the evaluation
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval 
  


# getting the best move for the current player using minimax algorithm
def get_best_move(board, depth):
    best_move = None
    if board.turn == chess.WHITE:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
    return best_move


if __name__ == "__main__":
    board = chess.Board()
    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            move = input("Enter your move in UCI format (e.g., e2e4): ")
            try:
                board.push_san(move)
            except ValueError:
                print("Invalid move. Please try again.")
        else:
            print("Talalfish is thinking...")
            ai_move = get_best_move(board, 3)
            board.push(ai_move)
    print("Game over:", board.result())