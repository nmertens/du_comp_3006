# import packages
import sys
import random

def get_card():
    ''' generate random integer
    '''
    return random.randint(1, 13)

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
    
    return(total, soft_ace_count)

def stand(stand_on_value, stand_on_soft, cards):
    ''' Stand (True) or Hit (False) depending on rules
    '''
    total, soft_ace_count = score(cards)

    # hand is soft
    if soft_ace_count == 1:
        # below stand on value = HIT
        if total < stand_on_value:
            return False 
        # at stand on value AND hit on soft = HIT
        elif (total == stand_on_value) & (stand_on_soft == False):
            return False 
        # at stand on value AND stand on soft = STAND
        elif (total == stand_on_value) & (stand_on_soft == True):
            return True
        # above stand on value = STAND
        elif total > stand_on_value:
            return True
    # hand is hard
    else:
        # below stand on value = HIT
        if total < stand_on_value:
            return False
        # at or above stand on value = STAND
        elif total >= stand_on_value:
            return True

def main():
    ''' simulate n poker hands
    '''

    # validate input
    # num_simulations
    try:
        num_simulations = int(sys.argv[1])
    except ValueError:
        print("ValueError: Oops! Did you input a string? Please, input an integer")
    # stand_on_value
    try:
        stand_on_value = int(sys.argv[2])
    except ValueError:
        print("ValueError: Oops! Did you input a string? Please, input an integer")
        
    #strategy
    strategy = str(sys.argv[3])

    if (strategy != "soft") & (strategy != "hard"):
        raise ValueError("Oops! You have to input either 'soft' or 'hard'.")
    

    # soft strategy = stand on soft, hard strategy = hit on soft
    if strategy == 'soft':
        stand_on_soft = True
    elif strategy == 'hard':
        stand_on_soft = False

    # initialize the number of times player has bust
    bust = 0

    # number of simulations
    for i in range(num_simulations):
        hand = [get_card(), get_card()] # initialize the hand
        total = score(hand)[0]
        #print("starting hand:", total) # optional: view the hand 
        hit_or_stand = stand(stand_on_value, stand_on_soft, hand)
        # hit (False)
        while hit_or_stand == False:
            hand.append(get_card())     # add a card
            total = score(hand)[0]      # get the total
            hit_or_stand = stand(stand_on_value, stand_on_soft, hand)
            #print("new hand:", total)  # optional: view the hand
        # stand (True)
        else:
            # did the player bust? if so add 1 to bust counter
            if total > 21:
                bust += 1

    print("Bust Percentage:", (bust/num_simulations)*100, "%")
    
if __name__ == '__main__':
    main()

