# learn21

**learn21** is a Blackjack simulation game built in Python that integrates classic card game logic with statistical decision-making and AI. The game features Monte Carlo simulations to evaluate risk and uses OpenAI's GPT model to help the dealer make human-like decisions.

## Features

* Object-oriented design with `Card`, `Deck`, and `Hand` classes
* Monte Carlo simulation (10,000 trials) to estimate bust probability
* AI dealer powered by OpenAI's GPT (via API call)
* Player can choose to hit or stand based on simulation results
* Dealer follows rules but can override with statistical advantage
* Option to reset the deck between rounds
* Clean console output and structured gameplay flow

## Requirements

* Python 3.7+
* OpenAI Python SDK (`openai`)
* Internet connection for GPT API usage

## Setup

1. Clone the repository or copy the code to a `.py` file:

```bash
git clone [https://github.com/yourusername/learn21.git](https://github.com/Eibon1108/Learn21)
cd learn21
```

2. Install dependencies:

```bash
pip install openai
```

3. Replace the placeholder API key in the code with your actual OpenAI key:

```python
client = OpenAI(api_key="sk-...")
```

4. Run the script:

```bash
python blackjack.py
```

## How It Works

### Player Turn

* Player is shown their hand and one of the dealer’s cards.
* Monte Carlo simulation estimates risk if the player hits.
* Player chooses whether to hit or stand.

### Dealer Turn

* Dealer hand is evaluated via Monte Carlo simulation.
* GPT-based dealer uses the statistical result to choose to hit or stand.
* Dealer continues until they bust or choose to stand.

### End of Round

* Results are shown for both hands.
* Player is prompted to play again or reset the deck.

## Notes

* Aces are automatically adjusted to avoid busts when possible.
* The Monte Carlo method simulates one-card draws to predict bust likelihood.
* GPT model used is `gpt-3.5-turbo` with low temperature for consistent decisions.

## Authors

Ismail Peracha, Ivan Perez, & Kaitlyn Lee
