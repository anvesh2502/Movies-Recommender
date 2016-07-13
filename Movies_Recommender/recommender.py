
import sample_data
from math import sqrt

def sim_distance_euclidean(prefs,person1,person2) :

    si={}

    for item in prefs[person1] :
      if item in prefs[person2] :
          si[item]=1

    #if there are no ratings common,return 0
    if len(si)==0 :
         return 0

     #Add up the squares of all the differences

    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sum_of_squares)

def sim_distance_pearson(prefs,p1,p2) :

    si={}

    for item in prefs[p1] :
        if item in prefs[p2] :
            si[item]=1

    n=len(si)

    if n==0 :
        return 0

    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    num=pSum-(sum1*sum2/n)

    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

    if den==0 :
        return 0

    r=num/den

    return r

def topMatches(prefs,person,n=5,similarity=sim_distance_pearson) :

    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

    scores.sort()
    scores.reverse()

    return scores[0:n]


def transformPrefs(prefs) :

    result={}

    for person in prefs :

        for item in prefs[person] :

            result.setdefault(item,{})
            result[item][person]=prefs[person][item]

    return result


def calculateSimilarItems(prefs,n=10) :

    result={}


    itemPrefs=transformPrefs(prefs)


    c=0

    for item in itemPrefs :
        c+=1
        if c%100==0 :
            print '%d / %d' % (c,len(itemPrefs))
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance_pearson)
        result[item]=scores
    return result



def getRecommendedItems(prefs,itemMatch,user) :

    userRatings=prefs[user]
    scores={}
    totalSim={}

    # Loop over items rated by this user

    for (item,rating) in userRatings.items() :

        # Loop over items rated by this user :

        for (similarity,item2) in itemMatch[item] :

            if item2 in userRatings :
                continue

            # Weighted sum of rating times similarity

            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            # Sum of all the similarities

            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # Dividing each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item) for item,score in scores.items()]

    # Sorting the rankings from highest to lowest

    rankings.sort()
    rankings.reverse()
    return rankings

#itemsim=calculateSimilarItems(sample_data.critics)
#print getRecommendedItems(sample_data.critics,itemsim,'Toby')

def getRecommendations(prefs,person,similarity=sim_distance_pearson) :

    totals={}
    simSums={}

    for other in prefs :

        if other==person : continue

        sim=similarity(prefs,person,other)

        if sim<=0 : continue

        for item in prefs[other] :

            if item not in prefs[person] or prefs[person][item]==0 :

                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim

    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings
