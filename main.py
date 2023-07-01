import pandas as pd
import predictor

wordle_words = pd.read_csv(
    'datasets/five-letter-words.csv')
df = pd.DataFrame(wordle_words)
wordList1 = df.values.tolist()
wordList = []

trial = 0
correct = False

def main():
    pred = predictor.Predictor()
    while(correct == False):
        if pred.trial == 0:
            pred.word='salet'
            print(pred.word) 
            # input
            a, b, c, d, e = map(int, input().split(' '))
            pred.scores = [a, b, c, d, e]
            pred.trial += 1
        else:
            print(pred.predict())
            a, b, c, d, e = map(int, input().split(' '))
            pred.scores = [a, b, c, d, e]
            pred.trial += 1

main()