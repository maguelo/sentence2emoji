'''

@author: Miguel Maldonado
'''
#!/usr/bin/env python

from setuptools import  setup

setup(name='sentence2emoji',
      version='1.0',
      description='Sentence to emoji',
      author='Miguel Maldonado',
      author_email='miguelangelmal@gmail.com',
      url='https://app.swaggerhub.com/apis-docs/Maguelo/sentence2emoji/0.1',
      packages=['sentence2emoji'],
      install_requires=["Flask==1.0.2","Flask-RESTful==0.3.6","h5py==2.8.0","Keras==2.2.2","numpy==1.14.5","tensorflow-gpu==1.10.1"],
     )


