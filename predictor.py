import pandas as pd
import math
from wolframclient.evaluation import WolframLanguageSession
import wolframalpha
from wordfreq import word_frequency

class Predictor:
    def __init__(self):
        # self.wordle_words = pd.read_csv('five-letter-words.csv')
        self.wordle_words = pd.read_csv("possible_words.csv")
        self.df = pd.DataFrame(self.wordle_words)
        #self.wordList = self.df.values.tolist()
        self.wordList = self.df
        self.correct = False
        self.trial = 0
        self.word = str()
        self.scores = []
        self.wlSize = self.wordList.shape[0]
        self.goodLetters = []
        self.uncertainty = 11.17
        self.placedLetters = []

    def predict(self):
        self.wordList = self.generateFilteredList(self.scores, self.word)

        self.word = self.getWord()
        self.trial += 1
        return self.word
        # print(self.wordList)
        # print(self.patterns)
        # import pdb; pdb.set_trace()
        # print(self.wordList)
        # input
        
        
    def generateFilteredList(self, scores, word):
        scores = list(scores)
        index = 0
        temp = self.wordList
        # drop the last word since when predict() is called it means that the last word didn't work
        temp = self.dropWord(temp, word)
        for score in self.scores:
            letter = word[index]
            match score:
                case 0:
                    if letter not in self.goodLetters and letter not in self.placedLetters and len(temp) > 1:
                        temp = self.filterBadLetters(letter, temp)
                case 1:
                        temp = self.filterGoodLetters(letter, index, temp)
                case 2:
                    if len(temp) > 1:
                        temp = self.filterPlacedLetters(letter, index, temp)
            
            # print(f'CHECKING INDEX{index}')
            # print(temp[:10])
            index += 1
        
        return temp

    def filterBadLetters(self, letter, words):
        # filters out words with incorrect letters
        words = words.values.tolist()
        word1 = list()
        # result = words
        # a = 0  # row number
        # for i in result.index:
        #     if (result.iloc[a].str.contains(letter).bool()):  # check if a dataframe does not contain bLetters
        #         result = result.drop(labels=i, axis=0)
        #         a -= 1  # deleted 1 row which means there's -1 row in total
        #         # NOTE: dFrame word doesnt have all the index number, some are NaN, so the only way is to skip those index and do the .drop()

        #     a += 1
        # return result
        for word in words:
            if str(letter) not in word[0]:
                word1.append(word)
        return pd.DataFrame(word1, columns=['WORDS'])

    def filterGoodLetters(self, letter, index, words):
        # filters out words with good letters but in wrong place
        # check for good words
        words = words.values.tolist()
        word1 = list()
        #words.reset_index()
        for word in words:
            if (str(letter) in word[0] and (word[0][index] != letter)):
                word1.append(word)
        self.goodLetters.append(letter)
        return pd.DataFrame(word1, columns=['WORDS'])

    def filterPlacedLetters(self, letter, index, words):
        if letter not in self.placedLetters:
            self.goodLetters.append(letter)
        words = words.values.tolist()
        word1 = list()
        for word in words:
            # if word.count(letter) == 1:
            #     if (letter in word[0]) and (word[0].index(str(letter)) == index):
            #         word1.append(word)
            #         runtime += 1
            # else:
            #     if (letter in word[0]) and ((word[0][word[0].index(str(letter)):].index(str(letter)) == index)):
            #         word1.append(word)
            #         runtime += 1
            index = int(index)
            if word[0][index] == letter:
                word1.append(word)

        
        # if runtime == 0:
        #     return pd.DataFrame(words, columns=['WORDS'])

        return pd.DataFrame(word1, columns=['WORDS'])

    def getSumPossibilities(self, word):
        # num = 0
        # for pattern in self.patterns:
        #     # print(self.generateFilteredList(pattern, word))
        #     print(num)
        #     num = num + self.generateFilteredList(pattern, word).shape[0]

        # return num
        num = sum([self.generateFilteredList(pattern, word).shape[0] for pattern in self.patterns])
        return num


    def calculate_entropy(self, word):
        # Start a Wolfram Language session
        # session = WolframLanguageSession()
        # probability = session.evaluate(f'WordFrequencyData["{word}"]')
        # client = wolframalpha.Client('bobchenchenzhibo@gmail.com')
        # result = client.query(f'WordFrequencyData["{word}"]')
        # probability = result['FrequencyData']['TotalFrequency']
        probability = float(word_frequency(word, 'en', wordlist='best', minimum=0.0))
        if probability == 0:
            return 0
        # calculate the entropy of the word
        entropy = 0
        entropy += probability * math.log2(probability)
        # session.terminate()

        return -entropy
    
    def getWord(self):
        words = self.wordList.values.tolist()
        maxEntropy = 0
        resultWord = str()
        for word in words:
            # temp = self.calculate_entropy(word[0])
            probability = float(word_frequency(word[0], 'en', wordlist='best', minimum=0.0))
            temp = probability * (self.trial + 1) + ((1 - probability) * ((self.trial + 1) + (self.uncertainty - self.calculate_entropy(word[0]))))
            if temp > maxEntropy:
                maxEntropy = temp
                resultWord = word[0]
                self.uncertainty -= temp
        return resultWord

    def dropWord(self, word_list, word):
        # Drop the rows that match the given word
        result = word_list[word_list.iloc[:,0] != word]
        return result