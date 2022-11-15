# import packages
import sys
import random
import collections
import csv

def get_card():
    ''' generate random integer
    '''
    return random.randint(1, 13)

# create a namedtuple object for score
Score = collections.namedtuple('Score', 'total soft_ace_count')

def score(cards):
    ''' take in a list of blackjack cards and return total sum and soft_ace_count
    '''
    # initializing counts
    soft_ace_count = 0
    total = 0
    
    # face cards values
    face_cards = (11, 12, 13)
    
    # check for aces
    ace = False
    if 1 in cards:
        ace = True

    # count the cards (treat all aces as hard)
    for card in cards:
        if card in face_cards:
            total += 10
        else:
            total += card
    
    # if aces present and would not bust make one ace soft
    if ace and total + 10 < 22:
        total += 10
        soft_ace_count += 1

    return Score(total, soft_ace_count)

# create namedtuple object for stand
Stand = collections.namedtuple('Stand', 'stand total')

def stand(stand_on_value, stand_on_soft, cards):
    ''' Stand (True) or Hit (False) depending on rules
    '''
    # get the hand total and soft_ace_count
    total, soft_ace_count = score(cards)

    # if below stand on value = HIT
    if total < stand_on_value:
        stand = False
    # if above stand on value = STAND
    elif total > stand_on_value:
        stand = True
    # if on stand on value with no soft aces or stand on soft = STAND
    elif soft_ace_count == 0 or stand_on_soft == True:
        stand = True
    # if on stand on value and hit on soft = Hit
    else:
        stand = False

    return Stand(stand, total)

def play_hand(stand_on_value, stand_on_soft):
    ''' simulate one hand
    '''

    hand = [get_card(), get_card()] # initialize the hand
    stand_or_hit = stand(stand_on_value, stand_on_soft, hand)
    
    # hit (False)
    while stand_or_hit.stand == False:
        hand.append(get_card()) # add a card
        stand_or_hit = stand(stand_on_value, stand_on_soft, hand) # test new hand
    
    total = score(hand)[0]

    # return 22 if bust, return total otherwise
    if total >= 22:
        return 22
    else:
        return total

def main():
    ''' simulate n poker hands
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
        num_sims = int(sys.argv[1])
    except ValueError:
        print("ValueError: Oops! Did you input a string? Please, input an integer")
    # check to see if it's greater than 0
    try:
        num_sims > 0
    except ValueError:
        print("ValueError: Oops! Please make sure you input a positive integer for this argument")

    stand_on_values = [ x for x in range(13,22)] # stand on values
    strategies = ['hard', 'soft'] # strategies

    table = list() # initialize empty list

    # get column names as first row in table
    col_names = collections.deque([f'{x}' for x in range(13,22)])
    col_names.appendleft('STRATEGY')
    col_names.append('BUST')
    table.append(list(col_names))
    
    # iterate over stand on values
    for value in stand_on_values:
    
        # iterate over strategies
        for strategy in strategies:

            # soft strategy = stand on soft, hard strategy = hit on soft
            if strategy == 'soft':
                stand_on_soft = True
                strat_name = f'S{value}' # strategy name for table
            else:
                stand_on_soft = False
                strat_name = f'H{value}'
        
            results = collections.defaultdict(int) # initialize defaultdict
    
            # run it through the number of simulations
            for i in range(num_sims):
                total = play_hand(value, stand_on_soft)
                results[total] += 1

            # take total and get a rounded percentage for each key
            for k in results:
                results[k] = round(((results[k]/num_sims)*100),1)
        
            # create a deque that contains the percentages of all numbers
            percentages = collections.deque([f'{x[1]}' for x in sorted(results.items())])
        
            # filling in zeros for values below stand on value
            while len(percentages) < 10:
                percentages.appendleft('0.0')
        
            # append the strategy name
            percentages.appendleft(strat_name)
        
            # append a list of percentages
            table.append(list(percentages))

    # write table to a csv
    with open('output.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(table)

# call the main function
if __name__ == '__main__':
    main()