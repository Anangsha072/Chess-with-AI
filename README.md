♟️ Chess vs AI (Python + Pygame)

A graphical chess game where a human player competes against an AI opponent.
The game uses Pygame for the GUI and python-chess for chess logic.
The AI makes decisions using the Minimax algorithm with Alpha-Beta pruning.

🚀 Features

🎮 Play as White vs AI (Black).

🧠 AI opponent with Minimax + Alpha-Beta (depth = 3).

♟️ Handles legal moves, check, checkmate, stalemate.

✨ Highlights selected piece and its legal moves.

♕ Auto-promotion of pawns to queens.

✅ Simple, clean Pygame GUI.
▶️ How to Play

Run the game:

python minimax_chess.py


You play as White.

Click a piece, then click its destination square.

AI (Black) will automatically make its move.

Messages for Check, Checkmate, Stalemate appear on the screen.
🧠 AI Logic

Uses Minimax algorithm with Alpha-Beta pruning.

Evaluation is based on material balance:

Pawn = 1
Knight/Bishop = 3
Rook = 5
![ezgif-85a483828eb06f](https://github.com/user-attachments/assets/5a3a2c26-747c-42b2-9d22-0a175342e874)


Queen = 9

King = not scored (game ends before capture).
