import pandas as pd
import random

class WordleGame:
    
    def __init__(self, wordlist_path):
        self.wordlist_path = wordlist_path
        self.wordlist = pd.read_csv(self.wordlist_path, header=None)[0].tolist()
        self.word = random.choice(self.wordlist)
        self.attempts = 0
        
    def play(self, guess):
        self.attempts += 1
        if len(guess) != 5:
            raise ValueError('Guess must be a 5-letter word')
        if guess not in self.wordlist:
            return [0] * 5, False
        
        placed_letters = [1 if guess[i] == self.word[i] else 0 for i in range(5)]
        correct_letters = [1 if guess[i] in self.word and guess[i] != self.word[i] else 0 for i in range(5)]
        feedback = [2 if placed_letters[i] == 1 else correct_letters[i] for i in range(5)]
        if placed_letters == [1] * 5:
            return feedback, True
        return feedback, False
    