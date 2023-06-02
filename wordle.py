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
            
        feedback = []
        for i in range(5):
            if guess[i] == self.word[i]:
                feedback.append(2)  # Letter is correctly placed
            elif guess[i] in self.word:
                feedback.append(1)  # Letter is correct but not in the correct position
            else:
                feedback.append(0)  # Letter is incorrect
            
        if feedback == [2] * 5:
            return feedback, True
        return feedback, False
    