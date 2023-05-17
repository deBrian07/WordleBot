from wordle import WordleGame
import predictor

for i in range(100):
    game = WordleGame("possible_words.csv")
    pred = predictor.Predictor()
    print(f'Simulation #{i}: ')
    print(f'Actual word: {game.word}')
    word = str()
    while True:
        if pred.trial == 0:
            pred.word='crane'
        word = pred.word
        print(f'Guess{pred.trial + 1}: {word}')
        scores, end = game.play(word)
        print(f'Socres: {scores}')
        if end == True:
            print(f'Tries: {pred.trial + 1}')
            break
        pred.scores = scores
        word = pred.predict()
