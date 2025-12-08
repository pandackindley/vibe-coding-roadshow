# Connect4 Django Web App Documentation

## Overview
This project is a web-based implementation of Connect4 using Django. It allows two players to enter their names, take turns dropping red and black tokens, and automatically detects wins and draws.

## Core Functions
- **launcher(request)**: Renders the launcher page where players enter their names and start a new game.
- **start_game(request)**: Handles the main game logic:
  - Initializes the board and player names on new game.
  - Processes token drops, alternates turns, and updates the board.
  - Detects win and draw conditions.
  - Handles game reset (clears board, keeps names).
  - Passes board state, player names, winner/draw info to the template.
- **check_win(board)**: Checks for four-in-a-row horizontally, vertically, or diagonally.
- **check_draw(board)**: Checks if the board is full with no winner.

## UI Elements
- **Launcher Page (`launcher.html`)**: Form for player names and starting a new game.
- **Game Page (`game_started.html`)**:
  - Displays player names and a 6x7 Connect4 board.
  - Arrow buttons above each column to drop tokens (disabled after win/draw).
  - Red and black tokens rendered as colored circles.
  - Win/draw messages shown when appropriate.
  - Reset button to clear the board and restart the game.

## Session Management
- Board state, turn, and player names are stored in Django's session, so the game persists across requests.

## How to Run
1. Install dependencies: `pip install django`
2. Start the server: `python manage.py runserver`
3. Visit `http://localhost:8000/` to play.

## File Structure
- `connect4/views.py`: Game logic and view functions
- `connect4/templates/connect4/launcher.html`: Launcher UI
- `connect4/templates/connect4/game_started.html`: Game UI
- `connect4/urls.py`: URL routing
- `manage.py`, `settings.py`: Django project setup

## Extending the Game
- Add win history, player stats, or AI opponent
- Improve UI with animations or mobile support
- Add authentication for persistent player profiles

---
For questions or feedback, see the main project README or contact the maintainer.
