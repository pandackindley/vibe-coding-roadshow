def game_docs(request):
    return render(request, 'connect4/game_docs.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
import django

def hello_world(request):
    return HttpResponse(f"Hello, world! Django version: {django.get_version()}")

def launcher(request):
    return render(request, 'connect4/launcher.html')

def start_game(request):
    # Session-based board and turn management
    if 'board' not in request.session:
        request.session['board'] = [[None for _ in range(7)] for _ in range(6)]
        request.session['turn'] = 'R'  # R for Red, B for Black

    board = request.session['board']
    turn = request.session['turn']

    winner = None
    draw = False

    def check_win(board):
        # Check horizontal, vertical, and diagonal for 4 in a row
        for r in range(6):
            for c in range(7):
                token = board[r][c]
                if token is None:
                    continue
                # Horizontal
                if c <= 3 and all(board[r][c+i] == token for i in range(4)):
                    return token
                # Vertical
                if r <= 2 and all(board[r+i][c] == token for i in range(4)):
                    return token
                # Diagonal down-right
                if r <= 2 and c <= 3 and all(board[r+i][c+i] == token for i in range(4)):
                    return token
                # Diagonal up-right
                if r >= 3 and c <= 3 and all(board[r-i][c+i] == token for i in range(4)):
                    return token
        return None

    def check_draw(board):
        return all(cell is not None for row in board for cell in row)

    if request.method == 'POST':
        if 'player_red' in request.POST and 'player_black' in request.POST:
            # New game from launcher, set names
            request.session['player_red'] = request.POST['player_red']
            request.session['player_black'] = request.POST['player_black']
            board = [[None for _ in range(7)] for _ in range(6)]
            turn = 'R'
            request.session['board'] = board
            request.session['turn'] = turn
        elif 'reset' in request.POST:
            # Reset the board and turn, keep names
            board = [[None for _ in range(7)] for _ in range(6)]
            turn = 'R'
            request.session['board'] = board
            request.session['turn'] = turn
        elif 'fill_draw' in request.POST:
            # Fill the board with alternating tokens, no winner
            board = [[None for _ in range(7)] for _ in range(6)]
            for r in range(6):
                for c in range(7):
                    board[r][c] = 'R' if (r + c) % 2 == 0 else 'B'
            request.session['board'] = board
            request.session['turn'] = 'R'
        elif 'drop' in request.POST:
            col = int(request.POST['drop'])
            # Drop token in the selected column
            for row in reversed(board):
                if row[col] is None:
                    row[col] = turn
                    break
            winner = check_win(board)
            draw = check_draw(board) if not winner else False
            # Alternate turn only if no winner or draw
            if not winner and not draw:
                request.session['turn'] = 'B' if turn == 'R' else 'R'
            request.session['board'] = board

    # Check for winner/draw after every move
    if not winner:
        winner = check_win(board)
    if not winner:
        draw = check_draw(board)

    cols = range(7)
    player_red = request.session.get('player_red', 'Red')
    player_black = request.session.get('player_black', 'Black')
    return render(request, 'connect4/game_started.html', {
        'board': board,
        'cols': cols,
        'winner': winner,
        'draw': draw,
        'player_red': player_red,
        'player_black': player_black,
    })
