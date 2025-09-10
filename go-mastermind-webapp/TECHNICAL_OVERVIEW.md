
# Go Mastermind Web App: Technical Documentation

## Overview

This web app is a Go implementation of the classic Mastermind game. It uses Go's `net/http` package to serve a landing page and a game page, with game logic handled server-side and a simple HTML/JavaScript frontend.

## Structure

- **main.go**: Contains all server logic, game logic, and HTML templates.
- **MASTERMIND_RULES.md**: Describes the rules of Mastermind.
- **TECHNICAL_OVERVIEW.md**: This file.

## Key Components

### 1. Landing Page

- Served at `/`.
- Simple HTML page with a button to start a new game.

### 2. Game Page

- Served at `/game`.
- HTML/JS interface for entering guesses and viewing feedback.
- JavaScript sends guesses to the backend and updates the UI with results.

### 3. Game Logic

- Secret code is generated randomly from the set of colors (Red, Blue, Green, Yellow, Orange, Purple).
- Each guess is scored for black (correct color & position) and white (correct color, wrong position) pegs.
- Game state is stored in a global variable for demo purposes.

### 4. Backend Endpoints

- `/game`: Serves the game UI.
- `/guess`: Accepts POST requests with guesses, returns feedback as JSON.

## How It Works

- When a user visits `/game`, a new secret code is generated.
- The user submits guesses via the form; JavaScript sends them to `/guess`.
- The backend scores the guess and returns feedback.
- The frontend displays the history and result.

## Technologies Used

- Go (net/http, encoding/json, math/rand)
- HTML/CSS/JavaScript (embedded in Go)

## Notes

- This implementation is for demo/learning purposes. For production, use session management and separate files for templates/static assets.
- All code is in a single file for simplicity.

## Author

Vibe Coding Roadshow

## Technologies Used

- Go (net/http, encoding/json, math/rand)
- HTML/CSS/JavaScript (embedded in Go)

## Notes

- This implementation is for demo/learning purposes. For production, use session management and separate files for templates/static assets.
- All code is in a single file for simplicity.

## Author

Vibe Coding Roadshow
