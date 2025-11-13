import pandas as pd
from typing import List, Tuple
from utils import feedback_pattern, is_consistent, score_guess

###############################################################################
# Feedback and scoring utilities
###############################################################################

"""Predictor implementation using true information gain and exact feedback."""


###############################################################################
# Predictor class
###############################################################################


class Predictor:
    def __init__(self):
        # Load the solution list; keep as simple Python list for performance
        df = pd.read_csv("datasets/possible_words.csv", header=None)
        self.all_solutions: List[str] = df[0].astype(str).str.lower().tolist()

        # Candidates start as all solutions
        self.wordList: List[str] = list(self.all_solutions)

        # Runtime state
        self.correct = False
        self.trial = 0
        self.word = str()
        self.start_word = 'adieu'  # Keep default start word for compatibility
        self.scores: List[int] = []
        self.history: List[Tuple[str, List[int]]] = []

        # Legacy fields kept for compatibility (not used in new logic)
        self.wlSize = len(self.wordList)
        self.goodLetters = []
        self.uncertainty = 11.17
        self.placedLetters = []

    def predict(self):
        # First move: return the fixed start word
        if self.trial == 0:
            self.word = self.start_word
            self.trial += 1
            return self.word

        # Record the last guess feedback into history (if provided)
        if self.word and isinstance(self.scores, list) and len(self.scores) == 5:
            self.history.append((self.word, list(self.scores)))

        # Rebuild candidate list using full history consistency
        self.wordList = [w for w in self.all_solutions if is_consistent(w, self.history)]

        # Choose next guess using true information gain (negative expected size)
        self.word = self.getWord()
        self.trial += 1
        return self.word

    def getWord(self):
        """
        Pick the highest-scoring word among current candidates using score_guess.
        """
        candidates = self.wordList
        best_word = None
        best_score = float('-inf')

        for w in candidates:
            s = score_guess(w, candidates)
            if s > best_score:
                best_score = s
                best_word = w

        # Fallback: if no candidates available (shouldn't happen), pick start word
        return best_word if best_word is not None else self.start_word

    # Kept for compatibility (not used by the new logic)
    def dropWord(self, word_list, word):
        # This legacy method originally operated on DataFrames; preserved as no-op
        # equivalent over lists for compatibility.
        if isinstance(word_list, list):
            return [w for w in word_list if w != word]
        # If a DataFrame is ever passed, mimic the original filtering behavior
        try:
            return word_list[word_list.iloc[:, 0] != word]
        except Exception:
            return word_list
