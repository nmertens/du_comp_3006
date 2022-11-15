"""Unit tests for the blackjack program."""
import unittest

import blackjack3

class TestBlackjack(unittest.TestCase):

    def test_Hand_object(self):
        hand = blackjack3.Hand([3])
        self.assertEqual([3], hand.cards)
        self.assertEqual(3, hand.total)
        self.assertEqual(0, hand.soft_ace_count)
        self.assertEqual(False, hand.is_bust()) # should not be a bust

        hand = blackjack3.Hand([3,2])
        self.assertEqual([3,2], hand.cards)
        self.assertEqual(5, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([3,2,10])
        self.assertEqual([3,2,10], hand.cards)
        self.assertEqual(15, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([3,2,10,11])
        self.assertEqual([3,2,10,11], hand.cards)
        self.assertEqual(25, hand.total)
        self.assertEqual(0, hand.soft_ace_count)
        self.assertEqual(True, hand.is_bust()) # should be a bust

        hand = blackjack3.Hand([3,2,10,11,12])
        self.assertEqual([3,2,10,11,12], hand.cards)
        self.assertEqual(35, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([3,2,10,11,12,13])
        self.assertEqual([3,2,10,11,12,13], hand.cards)
        self.assertEqual(45, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

    def test_Hand_object_more(self): 
        hand = blackjack3.Hand([3,12])
        self.assertEqual(13, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([5,5,10])
        self.assertEqual(20, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([11,10,1])
        self.assertEqual(21, hand.total)
        self.assertEqual(0, hand.soft_ace_count)
        self.assertEqual(False, hand.is_blackjack()) # should not be a blackjack

        hand = blackjack3.Hand([1,5])
        self.assertEqual(16, hand.total)
        self.assertEqual(1, hand.soft_ace_count)

        hand = blackjack3.Hand([1,1,5])
        self.assertEqual(17, hand.total)
        self.assertEqual(1, hand.soft_ace_count)

        hand = blackjack3.Hand([1,1,1,7])
        self.assertEqual(20, hand.total)
        self.assertEqual(1, hand.soft_ace_count)

        hand = blackjack3.Hand([7,8,10])
        self.assertEqual(25, hand.total)
        self.assertEqual(0, hand.soft_ace_count)
        self.assertEqual(True, hand.is_bust()) # should be a bust


    def test_Hand_with_soft_aces(self):
        hand = blackjack3.Hand([1])
        self.assertEqual([1], hand.cards)
        self.assertEqual(11, hand.total)
        self.assertEqual(1, hand.soft_ace_count)

        hand = blackjack3.Hand([1,10])
        self.assertEqual([1,10], hand.cards)
        self.assertEqual(21, hand.total)
        self.assertEqual(1, hand.soft_ace_count)
        self.assertEqual(True, hand.is_blackjack()) # should be blackjack

        hand = blackjack3.Hand([1,2,3])
        self.assertEqual([1,2,3], hand.cards)
        self.assertEqual(16, hand.total)
        self.assertEqual(1, hand.soft_ace_count)
        self.assertEqual(False, hand.is_blackjack()) # should not be blackjack

        hand = blackjack3.Hand([1,2,3,1])
        self.assertEqual([1,2,3,1], hand.cards)
        self.assertEqual(17, hand.total)
        self.assertEqual(1, hand.soft_ace_count)

        hand = blackjack3.Hand([1,2,3,10])
        self.assertEqual([1,2,3,10], hand.cards)
        self.assertEqual(16, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([1,2,3,10,1])
        self.assertEqual([1,2,3,10,1], hand.cards)
        self.assertEqual(17, hand.total)
        self.assertEqual(0, hand.soft_ace_count)

        hand = blackjack3.Hand([1,3,7])
        self.assertEqual([1,3,7], hand.cards)
        self.assertEqual(21, hand.total)
        self.assertEqual(1, hand.soft_ace_count)
        self.assertEqual(False, hand.is_blackjack()) # should not be a blackjack

    def test_Strategy_values(self):
        strat = blackjack3.Strategy(16, True)
        self.assertEqual(16, strat.stand_on_value)
        self.assertEqual(True, strat.stand_on_soft)

        strat = blackjack3.Strategy(17, False)
        self.assertEqual(17, strat.stand_on_value)
        self.assertEqual(False, strat.stand_on_soft)

    def test_Strategy_stand(self):
        STAND_ON_SOFT = True
        HIT_ON_SOFT = False

        # below stand on value, never stand
        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,8])
        self.assertEqual(False, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([5,8])
        self.assertEqual(False, strat.stand(hand))

        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,7,3])
        self.assertEqual(False, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([5,7,3])
        self.assertEqual(False, strat.stand(hand))

        # at stand on value, and the hand is hard, should stand either way

        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,7,2,2])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([5,7,2,2])
        self.assertEqual(True, strat.stand(hand))

        # at stand on value, and the hand is hard (but contains an ace), should stand either way
        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,5,5,1])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([5,5,5,1])
        self.assertEqual(True, strat.stand(hand))

        # at stand on value, and the hand is soft
        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,1])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([5,1])
        self.assertEqual(False, strat.stand(hand))

        # above stand on value, always stand

        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([3,3,1])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, HIT_ON_SOFT)
        hand = blackjack3.Hand([3,3,1])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,5,3,4])
        self.assertEqual(True, strat.stand(hand))

        strat = blackjack3.Strategy(16, STAND_ON_SOFT)
        hand = blackjack3.Hand([5,5,3,4])
        self.assertEqual(True, strat.stand(hand))

if __name__ == '__main__':
    unittest.main()