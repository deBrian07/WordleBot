import pandas as pd
import random
from utils import feedback_pattern

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
        # Compute official Wordle feedback using shared helper
        fb = list(feedback_pattern(guess, self.word))
        if fb == [2] * 5:
            return fb, True
        return fb, False
    
