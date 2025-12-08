from django.test import TestCase
from django.urls import reverse

class Connect4DrawTest(TestCase):
    def setUp(self):
        self.start_url = reverse('start_game')
        self.launcher_url = reverse('launcher')

    def test_draw_condition(self):
        # Start a new game with player names
        response = self.client.post(self.start_url, {
            'player_red': 'Alice',
            'player_black': 'Bob',
        })
        self.assertEqual(response.status_code, 200)

        # Fill the board with alternating tokens, no winner
        session = self.client.session
        board = [[None for _ in range(7)] for _ in range(6)]
        turn = 'R'
        for r in range(6):
            for c in range(7):
                board[r][c] = 'R' if (r + c) % 2 == 0 else 'B'
        session['board'] = board
        session['turn'] = turn
        session.save()

        # Reload game page
        response = self.client.get(self.start_url)
        self.assertContains(response, "It's a draw!")
