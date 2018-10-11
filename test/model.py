'''

@author: Miguel Maldonado
'''
import unittest
import os
from sentence2emoji.model import SentimentAnalysis
from definitions import MODEL_PATH

class TestModel(unittest.TestCase):
    PATH_MODEL_FILE = os.path.join(MODEL_PATH,"model_test.json")
    PATH_WEIGHTS_FILE =os.path.join(MODEL_PATH,"weight_test.h5")

    def setUp(self):
        self.model = SentimentAnalysis.getInstance(TestModel.PATH_MODEL_FILE, TestModel.PATH_WEIGHTS_FILE)

    def tearDown(self):
        pass

    

    def testHappySentenceHappy(self):
        sentence = "I’m very happy that my team won the world cup!"
        
        output = self.model.prediction(sentence)
        self.assertGreater(output,0.5)
    
    
        
    def testSadSentenceSad(self):
        sentence = "I am sad today i am unhappy and ugly"
        
        output = self.model.prediction(sentence)
        self.assertLess(output,0.5)     

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()