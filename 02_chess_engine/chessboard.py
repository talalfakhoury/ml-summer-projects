import chess
import pygame
from Talalfish import get_best_move

# initialize pygame
pygame.init()

WIDTH, HEIGHT = 480, 480
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Talalfish Chess Engine")

font = pygame.font.SysFont("Apple Symbols", 52)

LIGHT = pygame.Color(240, 217, 181)
DARK = pygame.Color(181, 136, 99)
HIGHLIGHT = pygame.Color(100, 200, 100)


# black:  ♚ ♛ ♜ ♝ ♞ ♟ 
# White: ♔ ♕ ♖ ♗ ♘ ♙
symbols = {
    (chess.PAWN, chess.WHITE): "♙", (chess.KNIGHT, chess.WHITE): "♘", (chess.BISHOP, chess.WHITE): "♗",
    (chess.ROOK, chess.WHITE): "♖", (chess.QUEEN, chess.WHITE): "♕", (chess.KING, chess.WHITE): "♔",
    (chess.PAWN, chess.BLACK): "♟", (chess.KNIGHT, chess.BLACK): "♞", (chess.BISHOP, chess.BLACK): "♝",
    (chess.ROOK, chess.BLACK): "♜", (chess.QUEEN, chess.BLACK): "♛", (chess.KING, chess.BLACK): "♚"
}   


def draw_board(board, selected_square=None):
    for rank in range(8):
        for file in range(8):
            color = LIGHT if (rank + file) % 2 == 0 else DARK
            square = chess.square(file, 7 - rank)
            if square == selected_square:
                color = HIGHLIGHT
            pygame.draw.rect(screen, color, (file * SQUARE_SIZE, rank * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board.piece_at(square)
            if piece:
                text_color = (255, 255, 255) if piece.color == chess.WHITE else (0, 0, 0)
                text = font.render(symbols[(piece.piece_type, piece.color)], True, (50, 50, 50))
                screen.blit(text, (file * SQUARE_SIZE + 14, rank * SQUARE_SIZE + 10))

def main():
    board = chess.Board()
    selected_square = None
    running = True

    while running and not board.is_game_over():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.WHITE:
                x, y = pygame.mouse.get_pos()
                file = x // SQUARE_SIZE
                rank = 7 - (y // SQUARE_SIZE)
                clicked_square = chess.square(file, rank)

                if selected_square is None:
                    if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == chess.WHITE:
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        board.push(move)
                        selected_square = None
                        # AI plays after you
                        if not board.is_game_over():
                            print("Talalfish is thinking...")
                            ai_move = get_best_move(board, 3)
                            board.push(ai_move)
                    else:
                        selected_square = None

        draw_board(board, selected_square)
        pygame.display.flip()

    print("Game over:", board.result())
    pygame.quit()

if __name__ == "__main__":
    main()





