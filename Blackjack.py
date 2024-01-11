import random

class Player:
    def __init__(self, money):
        self.money = money
        self.points = 0
        self.hand = []
        self.count_ace = 0
    
    def add_card(self, card, card_value):
        self.hand.append(card)
        self.points += card_value
    
    def count_aces(self, card):
        if card[-1] == 'A':
            self.count_ace += 1

    def ace_value(self):
        if self.points > 21 and self.count_ace > 0:
                self.points -= 10
                self.count_ace -= 1

class Game:
    def __init__(self):
        self.deck = {'C2': 2, 'C3': 3, 'C4': 4, 'C5': 5, 'C6': 6, 'C7': 7, 'C8' : 8, 'C9': 9, 'C10': 10, 'CJ': 10, 'CQ': 10, 'CK': 10, 'CA': 11,
        'D2': 2, 'D3': 3, 'D4': 4, 'D5': 5, 'D6': 6, 'D7': 7, 'D8' : 8, 'D9': 9, 'D10': 10, 'DJ': 10, 'DQ': 10, 'DK': 10, 'DA': 11,
        'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8' : 8, 'S9': 9, 'S10': 10, 'SJ': 10, 'SQ': 10, 'SK': 10, 'SA': 11,
        'H2': 2, 'H3': 3, 'H4': 4, 'H5': 5, 'H6': 6, 'H7': 7, 'H8' : 8, 'H9': 9, 'H10': 10, 'HJ': 10, 'HQ': 10, 'HK': 10, 'HA': 11}
    
    def deal_card(self):
        key, val = random.choice(list(self.deck.items()))
        return key, val

print("Welcome to Blackjack!")
wallet = int(input("How much money did you bring with you to the casino? "))
player = Player(wallet)
dealer = Player(0)
game = Game()
deal = 1

def play_card(person):
    card, card_value = game.deal_card()
    game.deck.pop(card)
    out_of_play[card] = card_value
    person.count_aces(card)
    person.add_card(card, card_value)
    return card, card_value

while player.money > 0:
    #placing money on the game
    pot = 0
    surrender = False
    out_of_play = {}
    
    bet = int(input("How much would you like to bet? "))
    while bet < 0 or bet > player.money:
        bet = int(input("You can't bet that amount. Please enter a valid amount. "))
    pot += bet * 2
    player.money -= bet
    print("The pot is {pot}.".format(pot=pot))

    print("Deal {deal}.".format(deal=deal))

    #creates and prints player hand
    play_card(player)    
    play_card(player)
    player.ace_value()
    print("Your hand is {hand}. You have {points} points.".format(hand=player.hand, points=player.points))

    #creates dealer hand
    play_card(dealer)
    dealer_show_card, dealer_value_show = play_card(dealer)
    dealer.ace_value()
    print("The dealer shows {card}. You can see {points} points.".format(card=dealer_show_card, points=dealer_value_show))

    #player takes their turn
    while player.points < 21:
        turn_number = 1
        turn = input("Enter H for hit, ST for stay, or SU for surrender. ")
        turn = turn.upper()
        if turn == "H":
            play_card(player)
            player.ace_value()
            print("Your hand is {hand}. You have {points} points.".format(hand=player.hand, points=player.points))
            turn_number +=1
        elif turn == "ST":
            break
        elif turn == "SU" and turn_number == 1:
            player.money += (bet / 2)
            print("Deal surrenderred. You now have {wallet}.".format(wallet=player.money))
            surrender = True
            break
        else:
            print("Invalid input.")

    if player.points == 21 and not surrender:
        print("You win!")
        player.money += pot
        print("You now have ${wallet}.".format(wallet=player.money))
    elif player.points > 21:
        print("You lose...")
        print("You now have ${wallet}.".format(wallet=player.money))
    elif 17 < dealer.points < 21 and dealer.points > player.points:
        print("The dealer's hand is {hand}. They have {points} points.".format(hand=dealer.hand, points=dealer.points))
        print("You lose...")
        print("You now have ${wallet}.".format(wallet=player.money))

    #dealer takes their turn
    else:
        while dealer.points < 17:
            play_card(dealer)
            dealer.ace_value()
            print("The dealer's hand is {hand}. They have {points} points.".format(hand=dealer.hand, points=dealer.points))
        if dealer.points > 21 or player.points > dealer.points and not surrender:
            print("You win!")
            player.money += pot
            print("You now have ${wallet}.".format(wallet=player.money))
        else:
            print("You lose...")
            print("You now have ${wallet}.".format(wallet=player.money))
    
    #play another hand?
    play_again = input("Would you like to play another hand? Y for yes N for no ")
    play_again = play_again.upper()
    
    if play_again == "Y":
        #reset player
        player.hand = []
        player.points = 0
        player.count_ace = 0

        #reset dealer
        dealer.hand = []
        dealer.points = 0
        dealer.count_ace = 0

        #reset game factors
        deal +=1
        surrender = False
        game.deck.update(out_of_play)
        continue
    elif play_again == "N":
        print("Thank you for playing. Your final balance is ${wallet}.".format(wallet=player.money))
        break

if player.money <= 0:
    print("You are out of money. Thank you for playing")