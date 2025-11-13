from wordle import WordleGame
import predictor
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import sys

EPOCHS = 10000

steps = []
with tqdm(total=EPOCHS, ncols=80) as pbar:
    for i in range(EPOCHS):
        game = WordleGame("datasets/possible_words.csv")
        pred = predictor.Predictor()
        tqdm.write(f'Simulation #{i}: ')
        tqdm.write(f'Actual word: {game.word}')
        word = str()
        step = 0
        while True:
            word = pred.predict()
            tqdm.write(f'Guess{pred.trial}: {word}')
            scores, end = game.play(word)
            score = []
            for i in scores:
                if i == 1:
                    score.append('🟨')
                elif i == 0:
                    score.append('⬜️')
                elif i == 2:
                    score.append('🟩')
            tqdm.write(f'Scores: {score}')
            if end:
                tqdm.write(f'Tries: {pred.trial}')
                steps.append(pred.trial)
                break
            pred.scores = scores
            step += 1
        tqdm.write(f'AVERAGE STEPS: {np.mean(steps)}')
        pbar.update(1)

# Creating Frequency Graph
plt.hist(steps, bins=[1,2,3,4,5,6,7])
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Frequency Graph')
plt.show()
