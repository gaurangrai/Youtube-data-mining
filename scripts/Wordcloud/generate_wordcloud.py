from os import path
import numpy as np
from PIL import Image
#from wordcloud import WordCloud, STOPWORDS
from wordcloud import WordCloud,STOPWORDS
import csv

# get path to script's directory
currdir = path.dirname(__file__)

def readCSV(filename):
    merged =""
    with open(filename) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            string = row[4].lower()
            merged+=" "+string
            
    return merged.strip()   


def create_wordcloud(text,filename,stopwords):
    # create numpy array for wordcloud mask image
    mask = np.array(Image.open(path.join(currdir, "cloud.png")))
    

    # create wordcloud object
    wc = WordCloud(background_color="white",
                    max_words=200,
                    mask=mask,
                       stopwords=stopwords)

    # generate wordcloud
    wc.generate(text)

    # save wordcloud
    wc.to_file(path.join(currdir, filename))
    print(filename + " generated")

if __name__== '__main__':    
    # create set of stopwords
    stopwords = set(STOPWORDS)
    
    file = open("stopwords_list.txt","r+")
    other_stopwords =  file.read().split(",")
    
    for word in other_stopwords:
        stopwords.add(word)
    
    filenames = ["../../csv_files/comments_comedy.csv","../../csv_files/comments_tech.csv","../../csv_files/comments_news.csv","../../csv_files/comments_TV.csv"]
    targetnames = ["comedy_wc.png","tech_wc.png","news_wc.png","tv_wc.png"]
    
    for i,filename in enumerate(filenames):
        text = readCSV(filename)
        create_wordcloud(text,targetnames[i],stopwords);



        