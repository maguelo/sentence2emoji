'''
 
@author: Miguel Maldonado
'''
import unittest
from sentence2emoji.service import app,users
from sentence2emoji.model import SentimentAnalysis
import os
import sys
import json
from definitions import MODEL_PATH
  
class TestService(unittest.TestCase):
    
    PATH_MODEL_FILE = os.path.join(MODEL_PATH,"model_test.json")
    PATH_WEIGHTS_FILE =os.path.join(MODEL_PATH,"weight_test.h5")

    def setUp(self):
        self.model = SentimentAnalysis.getInstance(TestService.PATH_MODEL_FILE, TestService.PATH_WEIGHTS_FILE)

        self.app = app.test_client()
        
        users["Nicholas"]={"emoji":"😁"}
        users["Elvin"]={"emoji":None}
        users["Jass"]={"emoji":None}
 
    def tearDown(self):
        users["Nicholas"]={"emoji":"😁"}
        users["Elvin"]={"emoji":None}
        users["Jass"]={"emoji":None}
        
    
        
    
    
    
    # test method
    def testGetNicholas(self):
        response = self.app.get('/bot/Nicholas')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': {'emoji': '😁'}})

    def testPostNicholasSentence(self):
        response = self.app.post('/bot/Nicholas',data=json.dumps({'sentence':'I am funny day was happy'}),
                       content_type='application/json')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': '😁'})
      
    def testPostNicholasFavourite(self):
        response = self.app.post('/bot/Nicholas',data=json.dumps({'sentence':'What is my favourite emoji?'}),
                       content_type='application/json')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': 'Your favourite emoji is 😁'})
         
    def testPostNicholasStore(self):
        response = self.app.post('/bot/Nicholas',data=json.dumps({'sentence':'My favourite emoji is 😥'}),
                       content_type='application/json')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': 'OK!'})
        self.assertEqual(users['Nicholas'],{'emoji': '😥'})
    
    def testPutJhon(self):
        response = self.app.put('/bot/Jhon')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': 'Add user Jhon to database'})
        self.assertEqual(users['Jhon'],{'emoji': None})
        
    def testDeleteNicholas(self):
        response = self.app.delete('/bot/Nicholas')
        output = json.loads(response.get_data().decode(sys.getdefaultencoding()))
        self.assertEqual(output,{'response': 'User Nicholas is deleted.'})
        
        self.assertFalse('Nicholas' in users.keys()) 
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSaveEmoji']
    unittest.main()