import chess
import random

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
        return 10
    elif piece.piece_type == chess.KNIGHT:
        return 30
    elif piece.piece_type == chess.BISHOP:
        return 30
    elif piece.piece_type == chess.ROOK:
        return 50
    elif piece.piece_type == chess.QUEEN:
        return 90
    elif piece.piece_type == chess.KING:
        return 900
    else:
        return 0
    

PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]

PIECE_TABLES = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
    chess.KING: KING_TABLE
}
    

# evaluate the board function + positional and material evaluation

def evaluate_board(board):
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_value(piece)
            if piece.color == chess.WHITE:
                evaluation += value + PIECE_TABLES[piece.piece_type][square]
            else:
                evaluation -= value + PIECE_TABLES[piece.piece_type][chess.square_mirror(square)]
    return evaluation 




# building simple model: 

# def minimax(board, depth):
#     if depth == 0 or board.is_game_over():
#         return evaluate_board(board)
    
#     # if white is playing, we want to maximize the evaluation
#     if board.turn == chess.WHITE:
#         max_eval = float('-inf')
#         for move in board.legal_moves:
#             board.push(move)
#             eval = minimax(board, depth - 1)
#             board.pop()
#             max_eval = max(max_eval, eval)
#         return max_eval
#     # if black is playing, we want to minimize the evaluation
#     else:
#         min_eval = float('inf')
#         for move in board.legal_moves:
#             board.push(move)
#             eval = minimax(board, depth - 1)
#             board.pop()
#             min_eval = min(min_eval, eval)
#         return min_eval 
  

# the current implementation is very basic and can be improved in many ways, such as adding more advanced evaluation functions, implementing alpha-beta pruning to optimize the minimax algorithm, and adding a transposition table to store previously evaluated positions.

def alpha_beta(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if board.turn == chess.WHITE:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    



# getting the best move for the current player using minimax algorithm
def get_best_move(board, depth):
    best_move = None
    moves = list(board.legal_moves)
    random.shuffle(moves)
    if board.turn == chess.WHITE:
        max_eval = float('-inf')
        for move in moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, float('-inf'), float('inf'))
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, float('-inf'), float('inf'))
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