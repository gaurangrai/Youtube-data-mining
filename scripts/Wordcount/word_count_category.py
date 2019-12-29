#!/usr/bin/env python3

import csv
import math
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS


stopwords = set(STOPWORDS)
csv_filepath = "../../csv_files/"
files = {"Tech": "comments_tech.csv","Comedy": "comments_comedy.csv","News":"comments_news.csv","TV":"comments_TV.csv"}
average_words_category = []

def count_words_with_file(filepath, category):
    totalRows = 0
    totalWords = 0
    comments = []
    
    with open(filepath, "r") as commentFile:
        commentReader = csv.reader(commentFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        for row in commentReader:
            comments.append(row[4].split())
            totalRows += 1
        
        for comment in comments:
            for word in comment:
                if word not in stopwords:
                    totalWords += 1

    return (category, int(math.floor(totalWords/totalRows)))

def plot_graph():
    xCoordinates = []
    yCoordinates = []
    xLabels = []
    counter = 1
    
    for val in average_words_category:
        xCoordinates.append(counter)
        yCoordinates.append(val[1])
        xLabels.append(val[0])
        counter += 1

    fig, ax = plt.subplots()

    rects = ax.bar(xCoordinates, yCoordinates, 0.75, color=['blue','green','red','yellow'])

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
            '%d' % int(height),
            ha='center', va='bottom')
        
        
    ax.set_title("Words Per Comment")
    ax.set_xticks(xCoordinates)
    ax.set_xticklabels(xLabels)
    ax.set_xlabel('Category')
    ax.set_ylabel('Words / Comment')

    plt.savefig('wordspercomment.png')



if __name__ == "__main__":
    
    # Calculating average words per comment for various categories
    for category,filename in files.items():
        average_words_category.append(count_words_with_file(csv_filepath+filename, category))

    # ploting a graph for the statistics collected
    plot_graph()




