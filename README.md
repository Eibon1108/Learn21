# learn21

**learn21** is a Blackjack simulation game built in Python that integrates classic card game logic with statistical decision-making and AI. The game features Monte Carlo simulations to evaluate risk and uses OpenAI's GPT model to help the dealer make human-like decisions.

## Features

- Object-oriented design with `Card`, `Deck`, and `Hand` classes
- Monte Carlo simulation (10,000 trials) to estimate bust probability
- AI dealer powered by OpenAI's GPT (via API call)
- Player can choose to hit or stand based on simulation results
- Dealer follows rules but can override with statistical advantage
- Option to reset the deck between rounds
- Clean console output and structured gameplay flow

## Requirements

- Python 3.7+
- OpenAI Python SDK (`openai`)
- Internet connection for GPT API usage

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Eibon1108/Learn21.git
cd learn21
```

2. Install dependencies:

```bash
pip install openai
```

3. Replace the placeholder API key in `blackjack.py` with your actual OpenAI key:

```python
client = OpenAI(api_key="sk-...")
```

4. Run the game:

```bash
python blackjack.py
```

## Code Layout

This project uses a modular layout:
### 'blackjack.py'
Contains the main game loop. Handles user interaction, round progression, and integrates other modules.

### `deck`
Contains:
- `Card` class: Represents a playing card
- `Deck` class: Manages a full deck (creation, shuffling, dealing, and resetting)

### `hand`
Contains:
- `Hand` class: Represents a hand of cards. Tracks value, manages aces, and can reset between rounds.

### `game functions`
Contains utility functions for gameplay:
- `hit_or_stand`, `hit`, `show_some`, `show_all`
- Win/loss message functions: `player_busts`, `dealer_busts`, `dealer_wins`, `player_wins`, `push`

### `monte_carlo.py`
Runs simulations to estimate the risk of busting:
- `run_simulations(deck, hand_value)` returns bust/stand probabilities

### `dealer_ai.py`
Handles the AI decision logic using OpenAI's GPT:
- `ask_llm_dealer_move(hand_value, sim_result)` returns "h" or "s" based on statistical insight


## How It Works

### Player Turn
- Player is shown their hand and one of the dealer’s cards
- Monte Carlo simulation estimates risk if the player hits
- Player chooses to hit or stand

### Dealer Turn
- Dealer simulates bust probability and makes decision using GPT
- Dealer either hits or stands based on AI output

### End of Round
- Game shows final hands
- Outcome is declared: win, lose, bust, or tie
- Player can choose to continue or quit

## Notes

- Aces are dynamically adjusted to avoid busting
- GPT model used is `gpt-3.5-turbo`, configured for consistent behavior
- The simulation assumes uniform card distribution for remaining cards

## Authors

Ismail Peracha, Ivan Perez, Kaitlyn Lee
