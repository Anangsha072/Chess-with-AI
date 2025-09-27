import pygame
import chess
import chess.engine
import random
import time

# Constants
WIDTH, HEIGHT = 512, 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
FPS = 60

WHITE = (245, 245, 220)
BLACK = (139, 69, 19)
HIGHLIGHT_COLOR = (186, 202, 68)

pygame.init()
FONT = pygame.font.SysFont("Arial", 32, True)


def load_images():
    pieces = ['P','N','B','R','Q','K','p','n','b','r','q','k']
    images = {}
    for piece in pieces:
        color = 'w' if piece.isupper() else 'b'
        images[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{color}{piece.upper()}.png"), (SQ_SIZE, SQ_SIZE)
        )
    return images


def draw_board(screen):
    colors = [WHITE, BLACK]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board, images):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            r = 7 - (square // 8)
            c = square % 8
            screen.blit(images[piece.symbol()], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_message(screen, message):
    text = FONT.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text, text_rect)


def highlight_squares(screen, board, selected_square):
    if selected_square is not None:
        r = 7 - (selected_square // 8)
        c = selected_square % 8
        s = pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, s, 4)

        piece = board.piece_at(selected_square)
        if piece and piece.color == board.turn:
            for move in board.legal_moves:
                if move.from_square == selected_square:
                    to_r = 7 - (move.to_square // 8)
                    to_c = move.to_square % 8
                    pygame.draw.circle(screen, HIGHLIGHT_COLOR,
                        (to_c * SQ_SIZE + SQ_SIZE // 2, to_r * SQ_SIZE + SQ_SIZE // 2), 10)


def draw_turn_info(screen, turn):
    msg = "Your Move" if turn == chess.WHITE else "AI Thinking..."
    info = FONT.render(msg, True, (0, 0, 0))
    screen.blit(info, (10, 10))


def evaluate_board(board):
    values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
              chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth-1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth-1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess vs AI")
    clock = pygame.time.Clock()
    images = load_images()

    board = chess.Board()
    player_color = chess.WHITE
    selected_square = None
    player_clicks = []
    running = True

    while running:
        draw_board(screen)
        highlight_squares(screen, board, selected_square)
        draw_pieces(screen, board, images)
        draw_turn_info(screen, board.turn)

        if board.is_checkmate():
            draw_message(screen, "Checkmate!")
        elif board.is_stalemate():
            draw_message(screen, "Stalemate!")
        elif board.is_check():
            draw_message(screen, "Check")

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == player_color:
                    location = pygame.mouse.get_pos()
                    file = location[0] // SQ_SIZE
                    rank = location[1] // SQ_SIZE
                    square = chess.square(file, 7 - rank)

                    if selected_square == square:
                        selected_square = None
                        player_clicks = []
                    else:
                        selected_square = square
                        player_clicks.append(square)

                    if len(player_clicks) == 2:
                        move = chess.Move(player_clicks[0], player_clicks[1])
                        if move in board.legal_moves:
                            if board.piece_at(move.from_square).piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
                                move.promotion = chess.QUEEN
                            board.push(move)
                        selected_square = None
                        player_clicks = []

        # AI move
        if board.turn != player_color and not board.is_game_over():
            time.sleep(0.5)  # Add delay for realism
            _, ai_move = minimax(board, 3, -float('inf'), float('inf'), True)
            if ai_move:
                board.push(ai_move)

    pygame.quit()


if __name__ == "__main__":
    main()



