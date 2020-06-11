"""
This is the card game of WAR.
A deck is created and shuffled, then it is split in half between two players.
Each player draws a card and the card with higher value wins. Winning player takes both cards.
In the case that the cards have the same value a WAR scenario is activated.
During hte war each player draws 4 more cards and their value is compared.
If the total of their 5 cards is still the same, then the players draw one card until the tie breaks.
Player with no remaining cards looses.
"""
import random

def deck_creator():
    sleeves = [" of Spades", " of Diamonds", " of Hearts", " of Clubs"]
    suit = "Ace Two Three Four Five Six Seven Eight Nine Ten Jack Queen King".split()
    deck = [x + y for y in sleeves for x in suit]
    # list comprehension, for each item in suits add each item in sleeves to it
    random.shuffle(deck)
    return deck

class playerCreator:
    def __init__(self, name='Computer', cards=[], total_points=0, turns_won=0):
        self.name = name
        self.cards = cards
        self.total_points = total_points
        self.turns_won = turns_won

    def play_card(self, num=1):
        """
        This method creates an empty list, which then is filled with cards from the cards list
        using the pop method. The amount of items or cards is defined by the parameter num.
        """
        played_cards = []
        while num != 0 and len(self.cards) != 0:
            played_cards += [self.cards.pop(0)]
            num -= 1
        return played_cards

    def won_turn(self, cards):
        """
        This method counts the number of turns won, adds the value of the cards to a total point score,
        and it takes in the list of cards played during the turn and appends each item, using a for loop,
        to the player cards list.
        """
        print(self.name, 'won this turn \n')
        self.turns_won += 1
        self.total_points += card_value(cards)
        self.cards.extend(cards)


def card_value(cards):
    """
    This function takes in a list of cards. It then takes each individual string value in the list, or card,
    and calculates its value by comparing the card string to the key in the dictionary, and grabbing the key value.
    Then it adds the value of each card to the variable sum.
    """
    sum = 0
    values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
              'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Ace': 11,
              'Jack': 12, 'Queen': 13, 'King': 14}
    for key in values:
        for card in cards:
            if key in card:
                sum += values[key]
    return sum

def higher_value(player_draw, computer_draw, computer, player):
    """
    This function takes in the two list of cards being played during the turn from the player and the computer.
    It also takes in the computer and player objects.
    It then prints the value of each player current cards, and compares to see who won the turn.
    """
    print('Player cards value: ', card_value(player_draw), 'Computer cards value: ', card_value(computer_draw))
    if card_value(player_draw) < card_value(computer_draw):
        computer_draw.extend(player_draw)
        computer.won_turn(computer_draw)

    elif card_value(player_draw) > card_value(computer_draw):
        player_draw.extend(computer_draw)
        player.won_turn(player_draw)

    elif card_value(player_draw) == card_value(computer_draw):
        """
        This is used if the value of the cards for both players is equal after a war scenario.
        Each player draws a card and is added to their turn card list.
        Then the list and objects are run again by calling this same function
        """
        print('War goes on! Draw again to end the war.\n')
        draw = input('Press enter to draw')
        player_draw += player.play_card()
        computer_draw += computer.play_card()
        print('{} flipped a '.format(player.name), player_draw)
        print('Cards remaining :', len(player.cards), '\n')
        print('Computer flipped a ', computer_draw)
        print('Cards remaining :', len(computer.cards), '\n')
        higher_value(player_draw, computer_draw, computer, player)

def game_start(compcards, playcards):
    # Create player and computer objects
    player = playerCreator(name=(input('What is your name?')), cards=playcards)
    computer = playerCreator(cards=compcards)

    def turns():
        turns_played = 0
        wars_fought = 0
        while len(player.cards) != 0 and len(computer.cards) != 0:
                                                            # While both players still have cards
            turns_played += 1
            player_draw = player.play_card()                # Draw a card using the object method
            computer_draw = computer.play_card()            # Draw a card using the object method
            print('\n--- Turn {} ---'.format(turns_played))
            draw = input('Press enter to draw')
            print('{} flipped a '.format(player.name), player_draw)
            print('Cards remaining :', len(player.cards), '\n')
            print('Computer flipped a ', computer_draw)
            print('Cards remaining :', len(computer.cards), '\n')

            if card_value(player_draw) == card_value(computer_draw):
                """
                This activates the war scenario explained in the beginning. 
                """
                print('Player cards value: ', card_value(player_draw),
                      'Computer cards value: ', card_value(computer_draw))
                wars_fought += 1
                print('\n --- WAR! ---\n')
                draw = input('Press enter to draw four cards') # This variable is only used as pause between turns
                player_draw.extend(player.play_card(4))
                print('{} flipped '.format(player.name), player_draw, '')
                computer_draw.extend(computer.play_card(4))
                print('Computer flipped ', computer_draw, '\n')
                higher_value(player_draw, computer_draw, computer, player) #send the values to the higher_value function
                                                                            #and restart the while loop.
                continue

            higher_value(player_draw, computer_draw, computer, player) #send the values to the higher_value function

        # Game ended by one player not having enough cards
        if len(player.cards) == 0:
            print('\nComputer has won the game\n')
        elif len(computer.cards) == 0:
            print('\n{} you won the game!\n'.format(player.name))
        # Summary of Game
        print('Turns Played: ', turns_played)
        print('Wars Played', wars_fought)
        print('Your Points: ', player.total_points)
        print('You won a total of ', player.turns_won, 'turns')
        print('Computer Points: ', computer.total_points)
        print('Computer won a total of ', computer.turns_won, 'turns')
        print('\n--- THANK YOU FOR PLAYING! ---')

    turns()

def split_deck():
    """
    This function first calls the deck creator function to create the deck, then it uses a while loop to give
    each player a card from the deck one by one until the deck is empty. Then it calls the game start function
    and passes the list of cards each player has.
    """
    deck = deck_creator()
    player_cards = []
    computer_cards = []
    while len(deck) != 0:
        player_cards.append(deck.pop(0))
        computer_cards.append(deck.pop(0))

    game_start(computer_cards, player_cards)

split_deck()