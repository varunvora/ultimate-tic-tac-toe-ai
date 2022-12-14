import unittest

from subboard import SubBoard


class TestSubBoard(unittest.TestCase):

    def test_is_board_full(self):
        b = SubBoard(3)
        self.assertFalse(b.is_board_full())
        b.play(1, (0, 0))
        self.assertFalse(b.is_board_full())
        b = SubBoard(3)
        player = 1
        for i in range(3):
            for j in range(3):
                # print(i, j, b)
                if (i, j) == (2, 0):
                    self.assertEqual(b.play(player, (i, j)), 1)
                    return
                self.assertIsNone(b.play(player, (i, j)))
                player = -1 if player == 1 else 1

    def test_get_winner(self):
        b = SubBoard(5)
        b.play(1, (0, 0))
        b.play(-1, (0, 1))
        b.play(1, (1, 0))
        b.play(-1, (0, 2))
        b.play(1, (2, 0))
        b.play(-1, (0, 3))
        b.play(1, (3, 0))
        b.play(-1, (0, 4))

        self.assertEqual(b.play(1, (4, 0)), 1)


if __name__ == '__main__':
    unittest.main()
