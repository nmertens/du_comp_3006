"""Unit tests for the blackjack program."""
import unittest

import blackjack2

class TestBlackjack(unittest.TestCase):

    def test_score_basic(self):
        ret = blackjack2.score([3])
        self.assertEqual((3, 0), ret)

        ret = blackjack2.score([3, 2])
        self.assertEqual((5, 0), ret)

        ret = blackjack2.score([3, 2, 10])
        self.assertEqual((15, 0), ret)

        # 11 counts as 10
        ret = blackjack2.score([3, 2, 10, 11])
        self.assertEqual((25, 0), ret)

        # 12 counts as 10
        ret = blackjack2.score([3, 2, 10, 11, 12])
        self.assertEqual((35, 0), ret)

        # 13 counts as 10
        ret = blackjack2.score([3, 2, 10, 11, 12, 13])
        self.assertEqual((45, 0), ret)

    def test_part_one_cases(self):
        self.assertEqual(blackjack2.score([ 3, 12 ]), (13, 0))
        self.assertEqual(blackjack2.score([ 5, 5, 10 ]), (20, 0))
        self.assertEqual(blackjack2.score([ 11, 10, 1 ]), (21, 0))
        self.assertEqual(blackjack2.score([ 1, 5 ]), (16, 1))
        self.assertEqual(blackjack2.score([ 1, 1, 5 ]), (17, 1))
        self.assertEqual(blackjack2.score([ 1, 1, 1, 7 ]), (20, 1))
        self.assertEqual(blackjack2.score([ 7, 8, 10 ]), (25, 0))

    def test_score_with_soft_aces(self):
        ret = blackjack2.score([1])
        self.assertEqual((11, 1), ret)

        ret = blackjack2.score([1,10])
        self.assertEqual((21, 1), ret)

        ret = blackjack2.score([1, 2, 3])
        self.assertEqual((16, 1), ret)

        ret = blackjack2.score([1, 2, 3, 1])
        self.assertEqual((17, 1), ret)

        ret = blackjack2.score([1, 2, 3, 10])
        self.assertEqual((16, 0), ret)

        ret = blackjack2.score([1, 2, 3, 10, 1])
        self.assertEqual((17, 0), ret)

    def test_stand_on_soft_rubric(self):
        STAND_ON_SOFT = True
        HIT_ON_SOFT = False
        # below stand on value, never stand
        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 8])
        self.assertEqual((False, 13), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 8])
        self.assertEqual((False, 13), ret)

        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 7, 3])
        self.assertEqual((False, 15), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 7, 3])
        self.assertEqual((False, 15), ret)

        # at stand on value, and the hand is hard, should stand either way
        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 7, 2, 2])
        self.assertEqual((True, 16), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 7, 2, 2])
        self.assertEqual((True, 16), ret)
        # at stand on value, and the hand is hard (but contains an ace), should stand either way
        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 5, 5, 1])
        self.assertEqual((True, 16), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 5, 5, 1])
        self.assertEqual((True, 16), ret)

        # at stand on value, and the hand is soft
        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 1])
        self.assertEqual((True, 16), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 1])
        self.assertEqual((False, 16), ret)
        # above stand on value, always stand
        ret = blackjack2.stand(16, STAND_ON_SOFT, [3, 3, 1])
        self.assertEqual((True, 17), ret)
    
        ret = blackjack2.stand(16, HIT_ON_SOFT, [3, 3, 1])
        self.assertEqual((True, 17), ret)

        ret = blackjack2.stand(16, STAND_ON_SOFT, [5, 5, 3, 4])
        self.assertEqual((True, 17), ret)

        ret = blackjack2.stand(16, HIT_ON_SOFT, [5, 5, 3, 4])
        self.assertEqual((True, 17), ret)

if __name__ == '__main__':
    unittest.main()
