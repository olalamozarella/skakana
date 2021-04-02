Python implementation of one of my favorite chess-like games!
"Skakana" is a Slovak name for a version of checkers where you don't capture any pawns - your sole goal is to get all your pawns to the other side of the chessboard. First player with all pawns on the other side wins!

You can play it yourself using simple TKinter chessboard, or enjoy AI vs AI fight.
Just pick the players:
- Human: human player that uses UI to do the moves
- Snake: AI player that can only move, not jump
- Frog: AI player that can move and do single jumps
- Kangaroo: AI player than can move and do multi jumps (single, double, triple)
First player plays as white, second as black - switch parameter order if you want to change colors.

To play manually run:
python3 main.py Human Human

This little game was created as a tool for developing simple AIs - to play with AI, run:
python3 Human Kangaroo

To let AIs play headless (useful for automated running/machine learning), run:
python3 Frog Kangaroo --headless

Beware - if you try to do an invalid move three consecutive times, you automatically lose! But don't worry, the same rule is also valid for AIs. Have fun!