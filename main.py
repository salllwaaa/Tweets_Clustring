import random as rd
import re
import math
from matplotlib import pyplot as plt

def pre_process_tweets(url):
    f = open(url)
    all_tweets = list(f)
    list_of_tweets = []

    for i in range(len(all_tweets)):
        all_tweets[i] = re.sub(r'@\S*.', "", all_tweets[i])
        all_tweets[i] = re.sub(r'#', "", all_tweets[i])
        all_tweets[i] = re.sub(r'www\S*.', "", all_tweets[i])
        all_tweets[i] = re.sub(r'http\S*.', "", all_tweets[i])
        all_tweets[i] = all_tweets[i][50:]
        all_tweets[i] = all_tweets[i].lower()
    f.close()
    print (all_tweets)
    return all_tweets


"""*****   jaccard      ******"""


def jaccard(tweet1, tweet2):

    union = set().union(tweet1, tweet2)
    intersection = set(tweet1).intersection(tweet2)
    dis = 1 - (len(intersection) / len(union))
    return dis


"""   ****     kmeans   *****       """


def k_means(k, max_itiration, tweets):
    prv_centroid = []
    itiration = 0
    centroids = []
    count = 0
    chek_random = []
    while count < k:
        random_tweet_idx = rd.randint(0, len(tweets) - 1)
        if random_tweet_idx not in chek_random:
            count += 1
            chek_random.append(random_tweet_idx)
            centroids.append(tweets[random_tweet_idx])

    while itiration < max_itiration:
     if convarge(prv_centroid, centroids) == True:
         break
     clusters = assign(centroids, tweets)
     prv_centroid = centroids
     centroids = update(clusters)
     """SSE"""
     sse = 0
     for i in range(len(clusters)):
         for j in range(len(clusters[i])):
             sse = sse + (clusters[i][j][1] * clusters[i][j][1])
     itiration += 1
    return sse, clusters


"""***cluster**"""


def assign(centroids, listoftweets):

    clusters=dict()
    indx =60

    for i in range(len(listoftweets)):
        min_dis=math.inf
        cluster_indx=-1
        for j in range(len(centroids)):
           dis=jaccard(centroids[j],listoftweets[i])

           if dis<min_dis:
               min_dis=dis
               cluster_indx=j
        if min_dis==1:
            cluster_indx=indx
            indx+=80
        clusters.setdefault(cluster_indx,[]).append([listoftweets[i]])
        #sse
        last_tweet_idx = len(clusters.setdefault(cluster_indx, [])) - 1
        clusters.setdefault(cluster_indx, [])[last_tweet_idx].append(min_dis)

    return clusters


"""** mean**"""


def update(clusters):
    new_centeroid = []
    for i in range(len(clusters)):
        redandant_dis = []
        min_dis = math.inf
        indx = -1
        for j in range(len(clusters[i])):
            redandant_dis.append([])
            dis_sum = 0
            for q in range(len(clusters[i])):

                if q < j:
                    dis = redandant_dis[q][j]
                elif q == j:
                    dis = 0
                else:
                    dis = jaccard(clusters[i][j][0], clusters[i][q][0])
                redandant_dis[j].append(dis)
                dis_sum += dis

            if dis_sum < min_dis:
                min_dis = dis_sum
                indx = j
        new_centeroid.append(clusters[i][indx][0])

    return new_centeroid


"""* convarge ***"""
def convarge(prv_centroid,new_centroid ):

    if len(prv_centroid)!=len(new_centroid):
        return False
    for i in range(len(new_centroid)):
        if new_centroid[i]!=prv_centroid[i]:
            return False
    return True
"""   main          """
if __name__ == '__main__':
    data_url = 'Health-Tweets/bbchealth.txt'
    tweets = pre_process_tweets(data_url)

    # default number of experiments to be performed
    experiments = 5

    # default value of K for K-means
    k = 3
    sse_list = []
    k_list =[]
    # for every experiment 'e', run K-means
    for e in range(experiments):

        print("------ Running K means for experiment no. " + str((e + 1)) + " for k = " + str(k))

        sse1,clusters = k_means(k,5,tweets)

        #for every cluster 'c', print size of each cluster
        for c in range(len(clusters)):
            print(str(c + 1) + ": ", str(len(clusters[c])) + " tweets")

        sse_list.append(sse1)
        print("--> SSE : " + str(sse1))
        print('\n')
        k_list.append(k)
        # increment k after every experiment
        k = k + 1

    plt.xlabel("k")
    plt.ylabel("SSE")
    plt.plot(k_list, sse_list)
    plt.show()