'''

@author: Miguel Maldonado
'''
import unittest
import os
from sentence2emoji.controller import detectSentenceType, storeEmoji, favoriteEmoji, controller
from sentence2emoji.model import SentimentAnalysis
from definitions import MODEL_PATH

class TestController(unittest.TestCase):
    
    PATH_MODEL_FILE = os.path.join(MODEL_PATH,"model_test.json")
    PATH_WEIGHTS_FILE =os.path.join(MODEL_PATH,"weight_test.h5")


    def setUp(self):
        self.users = {}
        self.users["Nicholas"]={"emoji":"😁"}
        self.users["Elvin"]={"emoji":None}
        self.users["Jass"]={"emoji":None}


        self.model = SentimentAnalysis.getInstance(TestController.PATH_MODEL_FILE, TestController.PATH_WEIGHTS_FILE)



    def tearDown(self):
        pass


    def testDetectFeeling(self):
        sentence="I’m very happy that my team won the world cup!"
        type_sentence = detectSentenceType(sentence)
        self.assertEqual(type_sentence, 0)
        
    def testSaveEmoji(self):
        sentence="My favourite emoji is 😁"
        type_sentence = detectSentenceType(sentence)
        self.assertEqual(type_sentence, 1)

    def testFavouriteEmoji(self):
        sentence="What is my favourite emoji?"
        type_sentence = detectSentenceType(sentence)
        self.assertEqual(type_sentence, 2)
        
    def testStoreEmoji(self):
        sentence="My favourite emoji is 😁"
        storeEmoji(sentence,"Elvin",self.users)
        self.assertEqual(self.users["Elvin"]["emoji"], "😁")                     

    def testFavoriteEmoji(self):
        output = favoriteEmoji("Nicholas",self.users)
        self.assertEqual(output, "Your favourite emoji is 😁")      
        
    def testControllerStore(self):
        sentence="My favourite emoji is 😁"
        output=controller(sentence,"Elvin",self.users,self.model)
        self.assertEqual(output, "OK!")
                       
    def testControllerFavouriteEmoji(self):
        sentence="What is my favourite emoji?"
        output= controller(sentence,"Nicholas",self.users,self.model)
        self.assertEqual(output,"Your favourite emoji is 😁")
        
    def testControllerSentimentHappy(self):
        sentence="I’m very happy that my team won the world cup!"
        output= controller(sentence,"Nicholas",self.users,self.model)
        self.assertEqual(output,'😁')
        
    def testControllerSentimentSad(self):
        sentence="I am sad today i am unhappy and ugly"
        output= controller(sentence,"Nicholas",self.users,self.model)
        self.assertEqual(output,'😥')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDetectFeeling']
    unittest.main()