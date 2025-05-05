import random
import time
import os
from openai import OpenAI

from openai import OpenAI

client = OpenAI(api_key="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")  # ✅ this creates the client properly


suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")
ranks = (
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
    "A",
)
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

playing = True

# CLASS DEFINTIONS:

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
                

    def __str__(self):
        deck_comp = ""  # start with an empty string
        for card in self.deck:
            deck_comp += "\n " + card.__str__()  # add each Card object's print string
        return "The deck has:" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        print("card removed! ",len(self.deck), " cards left")
        return single_card
    
    def deck_reset(self):
        self.__init__()
        self.shuffle()
        print("Deck Reset!")
        
        
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "A":
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
    def clear_hand(self):
        self.cards.clear()
        self.value = 0 
        print("hand emptied, ready for dealing")



# FUNCTION DEFINITIONS:

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    
    result = run_simulations(deck,hand.value)
    
    print(f"\n")
    print(f"Busts: {result['busts']}")
    print(f"Stands: {result['stands']}")
    print(f"Bust %: {result['bust_probability']:.2%}")
    print(f"Stand %: {result['stand_probability']:.2%}")

    while True:
        x = input("\nWould you like to Hit or Stand? Enter [h/s] ")

        if x[0].lower() == "h":
            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == "s":
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, Invalid Input. Please enter [h/s].")
            continue
        os.system('cls')
        break
    
def run_simulations(deck, hand_value, simulations=10000):
    current_total = hand_value
    busts = 0
    stands = 0

    # Card value lookup
    values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11
    }

    for _ in range(simulations):
        
        deck_copy = deck.deck[:] #make a copy of the deck 
        if not deck_copy:
            break  # Don't run if deck is empty
        
        random.shuffle(deck_copy) #added for more randomness
        card = random.choice(deck_copy)


        card_value = values[card.rank] #automatically revert the ace to 1 if the total crosses 21
        if card.rank == "A":
            card_value = 11 if current_total + 11 <= 21 else 1

        new_total = current_total + card_value

        if new_total > 21:    #where the bust comes from 
            busts += 1
        else:
            stands += 1        #where the stands come from 

    return {
        "busts": busts,
        "stands": stands,
        "bust_probability": busts / simulations,
        "stand_probability": stands / simulations
    }

def ask_llm_dealer_move(hand_value, monte_carlo_result):
    prompt = f"""
You are simulating a Blackjack dealer.

The dealer's current hand value is {hand_value}.
Monte Carlo results over 10,000 simulations show:
- Busts: {monte_carlo_result['busts']}
- Bust Probability: {monte_carlo_result['bust_probability']:.2%}
- Stands: {monte_carlo_result['stands']}
- Stand Probability: {monte_carlo_result['stand_probability']:.2%}

Based on standard Blackjack rules (dealer must hit below 17, stand at 17+), but feel free to use statistical advantage.

Respond with only one letter: "h" for Hit or "s" for Stand.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a blackjack dealer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=5
    )

    return response.choices[0].message.content.strip().lower()




def show_some(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print("", dealer.cards[1])


def show_all(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:", *dealer.cards, sep="\n ")
    print("Dealer's Hand =", dealer.value)


def player_busts(player, dealer):
    print("\n--- Player busts! ---")


def player_wins(player, dealer):
    print("\n--- Player has blackjack! You win! ---")


def dealer_busts(player, dealer):
    print("\n--- Dealer busts! You win! ---")


def dealer_wins(player, dealer):
    print("\n--- Dealer wins! ---")


def push(player, dealer):
    print("\nIts a tie!")
    



# GAMEPLAY!
print("\n----------------------------------------------------------------")
print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
print("                          Lets Play!")
print("----------------------------------------------------------------")
print(
    "Game Rules:  Get as close to 21 as you can without going over!\n\
    Dealer hits until he/she reaches 17.\n\
    Aces count as 1 or 11."
)


# Create & shuffle the deck, deal two cards to each player
deck = Deck()
deck.shuffle()

player_hand = Hand()
dealer_hand = Hand()
rounds = 0
    
while True:
    rounds+=1
    print("\nround: ", rounds)
    if rounds != 1:
        player_hand.clear_hand()
        dealer_hand.clear_hand()
    
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    while playing:  # game continues as long as this is true, playing getsset to false when the game is over
         # Show the cards:
        show_some(player_hand, dealer_hand)  # shows the player the hands both the player and dealer has
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)  #in this function if you go over 21 playing gets set to false automatically 
        
        if player_hand.value > 21:
            print("\nYour full hand:")
            print(*player_hand.cards, sep="\n ")
            print(f"your points are: ", player_hand.value)
            player_busts(player_hand, dealer_hand)
            break

    # If Player hasn't busted, play Dealer's hand
    if player_hand.value <= 21:

        # while dealer_hand.value < 17:
        #     hit(deck, dealer_hand)

        while True:
            sim_result = run_simulations(deck, dealer_hand.value)
            llm_decision = ask_llm_dealer_move(dealer_hand.value, sim_result)

            print(f"\nDealer LLM Decision: {llm_decision}")

            if llm_decision.lower() == "h":
                hit(deck, dealer_hand)
                if dealer_hand.value > 21:
                    break  # dealer busted
            else:
                break  # dealer stands

        # Show all cards
        time.sleep(1)
        print("\n----------------------------------------------------------------")
        print("                     ★ Final Results ★")
        print("----------------------------------------------------------------")

        show_all(player_hand, dealer_hand)

        # Test different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand)

        else:
            push(player_hand, dealer_hand)

    # Ask to play again
    new_game = input("\nPlay another hand? [Y/N] ")
    while new_game.lower() not in ["y", "n"]:
        new_game = input("Invalid Input. Please enter 'y' or 'n' ")
    if new_game[0].lower() == "y":
        new_deck = input("\nwould you like a new deck?[Y/N]")
        os.system('cls')
        playing = True
        if new_deck[0].lower() == "y":
            deck.deck_reset()
            continue
        continue
    else:
        print("\n------------------------Thanks for playing!---------------------\n")
        break
