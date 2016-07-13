
import sys
from load_data import loadMovieLens
from recommender import *


prefs=loadMovieLens()

user_num=raw_input('Please enter the user number :')

if user_num not in prefs :

  print 'User not available '
  sys.exit(1)

print getRecommendations(prefs,user_num)[0:5]  
