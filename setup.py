from setuptools import setup

setup(
   name='Sentiment Bot Detection',
   version='1.0',
   description='A useful module',
   author='Connate',
   author_email='cxnnate@gmail.com',
   packages=['senti-bot-detection'],  #same as name
   install_requires=['tweepy'], #external packages as dependencies
)