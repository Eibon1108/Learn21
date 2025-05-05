import random
import time
import os

suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")
ranks = (
    "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"
)
values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11,
}

playing = True

# -------- CLASS DEFINITIONS --------

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def __str__(self):
        return "The deck has:\n" + "\n ".join(str(card) for card in self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        print("Card removed! ", len(self.deck), " cards left")
        return single_card

    def deck_reset(self):
        self.__init__()
        self.shuffle()
        print("Deck Reset!")


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "A":
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def clear_hand(self):
        self.cards.clear()
        self.value = 0
        self.aces = 0
        print("Hand emptied, ready for dealing")


# -------- FUNCTION DEFINITIONS --------

def hit(deck, hand):
    hand.add_card(deck.deal())


def run_simulations(deck, hand_value, simulations=1000):
    busts = 0
    stands = 0
    remaining_deck = deck.deck[:]

    for _ in range(simulations):
        if not remaining_deck:
            break
        sim_card = random.choice(remaining_deck)
        card_val = values[sim_card.rank]
        if sim_card.rank == "A":
            card_val = 11 if hand_value + 11 <= 21 else 1
        total = hand_value + card_val
        if total > 21:
            busts += 1
        else:
            stands += 1

    return {
        "busts": busts,
        "stands": stands,
        "bust_probability": busts / simulations,
        "stand_probability": stands / simulations
    }


def dealer_decision(deck, dealer_hand, player_score):
    result = run_simulations(deck, dealer_hand.value)
    print(f"\n[Dealer AI] Bust %: {result['bust_probability']:.2%}, Stand %: {result['stand_probability']:.2%}")
    return "hit" if result["bust_probability"] < 0.4 else "stand"


def hit_or_stand(deck, hand):
    global playing
    result = run_simulations(deck, hand.value)
    print(f"\n[Player Hint] Bust %: {result['bust_probability']:.2%}, Safe %: {result['stand_probability']:.2%}")

    while True:
        x = input("Would you like to Hit or Stand? Enter [h/s] ")
        if x[0].lower() == "h":
            hit(deck, hand)
        elif x[0].lower() == "s":
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Invalid input. Please enter [h/s].")
            continue
        os.system('cls' if os.name == 'nt' else 'clear')
        break


def show_some(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:\n <card hidden>\n", dealer.cards[1])


def show_all(player, dealer):
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)
    print("\nDealer's Hand:", *dealer.cards, sep="\n ")
    print("Dealer's Hand =", dealer.value)


def player_busts():
    print("\n--- Player busts! ---")


def player_wins():
    print("\n--- Player wins! ---")


def dealer_busts():
    print("\n--- Dealer busts! Player wins! ---")


def dealer_wins():
    print("\n--- Dealer wins! ---")


def push():
    print("\nIt's a tie!")


# -------- GAMEPLAY --------

print("\n----------------------------------------------------------------")
print("                ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦")
print("                          Let's Play!")
print("----------------------------------------------------------------")
print(
    "Game Rules: Get as close to 21 as you can without going over!\n"
    "Dealer uses probability-based strategy.\nAces count as 1 or 11."
)

deck = Deck()
deck.shuffle()

player_hand = Hand()
dealer_hand = Hand()
rounds = 0

while True:
    rounds += 1
    print(f"\n--- Round {rounds} ---")
    if rounds != 1:
        player_hand.clear_hand()
        dealer_hand.clear_hand()

    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    while playing:
        show_some(player_hand, dealer_hand)
        hit_or_stand(deck, player_hand)

        if player_hand.value > 21:
            print("\nYour full hand:")
            print(*player_hand.cards, sep="\n ")
            print("Your points:", player_hand.value)
            player_busts()
            break

    if player_hand.value <= 21:
        while True:
            decision = dealer_decision(deck, dealer_hand, player_hand.value)
            if decision == "hit":
                print("\nDealer decides to HIT.")
                time.sleep(1)
                hit(deck, dealer_hand)
            else:
                print("\nDealer decides to STAND.")
                time.sleep(1)
                break

        print("\n----------------------------------------------------------------")
        print("                     ★ Final Results ★")
        print("----------------------------------------------------------------")
        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts()
        elif dealer_hand.value > player_hand.value:
            dealer_wins()
        elif dealer_hand.value < player_hand.value:
            player_wins()
        else:
            push()

    # Asks to play again
    new_game = input("\nPlay another hand? [Y/N] ")
    while new_game.lower() not in ["y", "n"]:
        new_game = input("Invalid input. Please enter [y/n]: ")

    if new_game[0].lower() == "y":
        new_deck = input("Would you like a new deck? [Y/N] ")
        playing = True
        if new_deck[0].lower() == "y":
            deck.deck_reset()
        os.system('cls' if os.name == 'nt' else 'clear')
        continue
    else:
        print("\n------------------------ Thanks for playing! ---------------------\n")
        break
