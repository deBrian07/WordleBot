from wordle import WordleGame
import predictor
import matplotlib.pyplot as plt
import numpy as np

steps = []
for i in range(1000):
    game = WordleGame("datasets/possible_words.csv")
    pred = predictor.Predictor()
    print(f'Simulation #{i}: ')
    print(f'Actual word: {game.word}')
    word = str()
    while True:
        word = pred.predict()
        print(f'Guess{pred.trial}: {word}')
        scores, end = game.play(word)
        score = []
        for i in scores:
            if i == 1:
                score.append('🟨')
            elif i == 0:
                score.append('⬜️')
            elif i == 2:
                score.append('🟩')
        print(f'Socres: {score}')
        if end == True:
            print(f'Tries: {pred.trial}')
            steps.append(pred.trial)
            break
        pred.scores = scores

print(f'AVERAGE STEPS: {np.mean(steps)}')

# Creating Frequency Graph
plt.hist(steps, bins=6)

plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Frequency Graph')

plt.show()