
import sys
from load_data import loadMovieLens
from recommender import *


prefs=loadMovieLens()

user_num=raw_input('Please enter the user number :')

if user_num not in prefs :

  print 'User not available '
  sys.exit(1)

movies=getRecommendations(prefs,user_num)

if len(movies)>10 :
    movies=movies[0:10]

print 'The Recommended movies to this user are : '
print

for movie in movies :
    print movie[1]
