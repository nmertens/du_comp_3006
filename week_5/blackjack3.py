import sys
import collections
import csv
import random

class Hand:
    ''' class that encapsulates a blackjack hand
    '''
    def __init__(self, cards = None):
        ''' initialize the hand
        '''
        # if input is given
        if cards is not None:
            self.cards = cards
            self.score()
        # if no input is given
        else:
            self.cards = []
            self.total = 0
            self.soft_ace_count = 0

    def __str__(self):
        ''' print out attributes
        '''
        print(f'Your cards are: {self.cards}')
        print(f'Point total: {self.total}')
        print(f'Number of soft aces: {self.soft_ace_count}')

    def add_card(self):
        ''' add a random card to the hand and re-score hand
        '''
        self.cards = self.cards + [random.randint(1,13)]
        self.score()

    def is_blackjack(self):
        ''' check if blackjack
        '''
        face_cards = [10,11,12,13]
        
        if any(card in self.cards for card in face_cards): # if any card in the hand is a face card
            if self.soft_ace_count > 0 and self.total == 21: # if other card is a soft ace
                return True 
            else:
                return False
        else:
            return False

    def is_bust(self):
        ''' check if player bust
        '''
        if self.total > 21:
            return True
        else:
            return False

    def score(self):
        ''' score the hand
        '''
        # initialize total and soft_ace_count
        self.total = 0
        self.soft_ace_count = 0

        # face cards values
        face_cards = (11, 12, 13)
    
        # check for aces
        ace = False
        if 1 in self.cards:
            ace = True

        # count the cards (treat all aces as hard)
        for card in self.cards:
            if card in face_cards:
                self.total += 10
            else:
                self.total += card
    
        # if aces present and would not bust make one ace soft
        if ace and self.total + 10 < 22:
            self.total += 10
            self.soft_ace_count += 1

class Strategy:
    ''' class that encapsulates a blackjack strategy
    '''
    def __init__(self, stand_on_value, stand_on_soft):
        ''' Strategy values
        '''
        self.stand_on_value = stand_on_value
        self.stand_on_soft = stand_on_soft

    def __repr__(self):
        ''' print out 'canonical' values
        '''
        print(f"Stand on value is: {self.stand_on_value}")
        print(f"Stand on soft aces? {self.stand_on_soft}")

    def __str__(self):
        ''' print out values
        '''
        if self.stand_on_soft == True: # soft strategy
            self.strategy = "S"
        else:                          # hard strategy
            self.strategy = "H"
        print(f"Strategy: {self.strategy}{self.stand_on_value}")

    def stand(self, hand):
        ''' Stand (True) or Hit (False) depending on rules
        '''
        # if below stand on value = HIT
        if hand.total < self.stand_on_value:
            stand = False
        # if above stand on value = STAND
        elif hand.total > self.stand_on_value:
            stand = True
        # if on stand on value with no soft aces or stand on soft = STAND
        elif hand.soft_ace_count == 0 or self.stand_on_soft == True:
            stand = True
        # if on stand on value and hit on soft = Hit
        else:
            stand = False
        # return True or False
        return stand
    
    def play(self):
        ''' play a hand of blackjack
        '''
        hand = Hand() # instantiate hand object

        while len(hand.cards) < 2: # add cards 
            hand.add_card()
        
        self.decision = self.stand(hand) # hit or stand?

        while self.decision == False: # continue until stand or bust
            hand.add_card()
            self.decision = self.stand(hand)

        return hand

def main():
    ''' simulate n blackjack hands
    '''
    # validate input
    # make sure there are correct number of inputs
    try:
        len(sys.argv) == 2
    except ValueError:
        print("ValueError: Oops! Please enter only the number of simulations you want to run.")
    # num_simulations
    # check to see if it's a number
    try:
        n = int(sys.argv[1])
    except ValueError:
        print("ValueError: Oops! Did you input a string? Please, input an integer")
    # check to see if it's greater than 0
    try:
        n > 0
    except ValueError:
        print("ValueError: Oops! Please make sure you input a positive integer for this argument")

    stand_on_values = [ x for x in range(13,21)] # stand on values
    strategies = ['H', 'S'] # strategies: H = hard, S = soft

    table = list() # initialize empty list

    # get column names as first row in table
    col_names = collections.deque(['P-Strategy'])
    for value in stand_on_values:
        for strategy in strategies:
            col_names.append(f"D-{strategy}{value}")
    table.append(list(col_names))

    # this section if for each of the player strategies
    for player_value in stand_on_values:
        for player_strategy in strategies:
        
            if player_strategy == 'H': # hard strategy = hit on soft
                player_stand_on_soft = False
                player_strat_name = f'P-H{player_value}'
            else:
                player_stand_on_soft = True # soft strategy = stand on soft
                player_strat_name = f'P-S{player_value}'
            
            # instantiate player strategy
            player_strat = Strategy(player_value, player_stand_on_soft)
            
            row = list() # initialize empty row
            row.append(player_strat_name)
        
            # this section is for each of the dealer strategies
            for dealer_value in stand_on_values:
                for dealer_strategy in strategies:
                
                    if dealer_strategy == 'H': # hard strategy = hit on soft
                        dealer_stand_on_soft = False
                    else:
                        dealer_stand_on_soft = True # soft strategy = stand on soft

                    # instantiate dealer strategy
                    dealer_strat = Strategy(dealer_value, dealer_stand_on_soft)
                
                    player_wins = 0 # initialize player wins

                    # loop over the number of simulations
                    for i in range(n):
                        player_hand = player_strat.play()
                        # player bust?: DEALER WINS
                        if player_hand.is_bust() == True:
                            next
                    
                        # play dealer's hand
                        dealer_hand = dealer_strat.play()
            
                        # dealer bust?: PLAYER WINS
                        if dealer_hand.is_bust() == True:
                            player_wins += 1
                        # player has blackjack and dealer doesn't: PLAYER WINS
                        elif player_hand.is_blackjack() == True and dealer_hand.is_blackjack() == False:
                            player_wins += 1
                        # dealer has blackjack and player doesn't: DEALER WINS
                        elif player_hand.is_blackjack() == False and dealer_hand.is_blackjack() == True:
                            next
                        # if both have 21, but player has blackjack and dealer doesn't: PLAYER WINS
                        elif player_hand.total == dealer_hand.total and player_hand.is_blackjack() == True:
                            player_wins += 1
                        # if both have 21, but dealer has blackjack and player doesn't: DEALER WINS
                        elif player_hand.total == dealer_hand.total and dealer_hand.is_blackjack() == True:
                            next
                        # player total equals dealer total: TIE
                        elif player_hand.total == dealer_hand.total:
                            next
                        # player hand greater than dealer hand: PLAYER WINS
                        elif player_hand.total > dealer_hand.total:
                            player_wins += 1
                        else:
                            next
                    row.append(round((player_wins/n)*100,2)) # append value to row
        
            table.append(row) # append row to table

    # write table to a csv
    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

# call the main function
if __name__ == '__main__':
    main()