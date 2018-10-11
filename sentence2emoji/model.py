'''
 
@author: Miguel Maldonado
'''

import numpy 
from numpy import array
from keras.datasets import imdb 
from keras.models import Sequential 
from keras.layers import Dense 
from keras.layers import Flatten
from keras.layers.embeddings import Embedding 
from keras.preprocessing import sequence 
from keras.models import model_from_json
import keras
import re
import os





numpy.random.seed(7)



class SentimentAnalysis():
    instance=None
    
    
    @staticmethod
    def getInstance(path_model="model.json",path_weights="model.h5"):
        if SentimentAnalysis.instance is None:
            SentimentAnalysis.instance = SentimentAnalysis()
            if path_model is not None and path_weights is not None:
                if os.path.exists(path_model)  and os.path.exists(path_weights):
                    SentimentAnalysis.instance.loadModel(path_model,path_weights)
            
            if SentimentAnalysis.instance.model is None:
                SentimentAnalysis.instance.trainModel()
                SentimentAnalysis.instance.saveModel(path_model, path_weights)
                
        return SentimentAnalysis.instance
            
    def __init__(self,top_words=5000,max_review_length=500,embedding_vector_length=32,special_char_list=['!']):
        self.top_words= top_words
        self.max_review_length = max_review_length
        self.embedding_vector_length = embedding_vector_length
        self.special_char_list = special_char_list
        
        self.word_to_id = self.__prepareWord()
            
        self.model = None

    def __prepareWord(self):
        INDEX_FROM=3   # word index offset
        word_to_id = keras.datasets.imdb.get_word_index()
        word_to_id = {k:(v+INDEX_FROM) for k,v in word_to_id.items()}
        word_to_id["<PAD>"] = 0
        word_to_id["<START>"] = 1
        word_to_id["<UNK>"] = 2
        return word_to_id

    def trainModel(self):
        #import data
        (X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=self.top_words)

        #preprocess data
        X_train = sequence.pad_sequences(X_train, maxlen=self.max_review_length) 
        X_test = sequence.pad_sequences(X_test, maxlen=self.max_review_length) 


        model = Sequential() 
        model.add(Embedding(self.top_words, self.embedding_vector_length, input_length=self.max_review_length)) 
        #model.add(LSTM(100)) 
        model.add(Flatten()) 
        model.add(Dense(1, activation='sigmoid')) 
        model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy']) 
        #print(model.summary()) 


        #train model
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3, batch_size=64) 

        #evaluate model
        scores = model.evaluate(X_test, y_test, verbose=0) 

        print("Accuracy: %.2f%%" % (scores[1]*100))
        self.model= model
    
    def __prepareSentence(self,sentence):
        sentence = sentence.lower()
        sentence = re.sub("|".join(self.special_char_list), "", sentence)
        return sentence
    
    def prediction(self,sentence):
        sentence = self.__prepareSentence(sentence)
        tmp = []
        for word in sentence.split(" "):
            tmp.append(self.word_to_id[word])

        tmp_padded = sequence.pad_sequences([tmp], maxlen=self.max_review_length) 
        
        return self.model.predict(array([tmp_padded][0]))[0][0]
    
    def saveModel(self, path_model="model.json",path_weights="model.h5"):
        # serialize model to JSON
        model_json = self.model.to_json()
        with open(path_model, "w") as json_file:
            json_file.write(model_json)
        
        # serialize weights to HDF5
        self.model.save_weights(path_weights)
        print("Saved model to disk")
    
    
    def loadModel(self,path_model="model.json",path_weights="model.h5"):
        # load json and create model
        json_file = open(path_model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        
        # load weights into new model
        self.model.load_weights(path_weights)        
        print("Loaded model from disk")
        