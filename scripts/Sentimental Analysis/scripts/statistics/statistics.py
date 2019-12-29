#!/usr/bin/env python3
import csv
import math
import matplotlib.pyplot as plt

filepath = "../prediction.csv"

answerPercentages = {}

stats = {"Tech": {"positive": 0, "negative": 0, "neutral": 0, "totalCount": 0 },
        "Comedy": {"positive": 0, "negative": 0, "neutral": 0, "totalCount": 0 },
        "News": {"positive": 0, "negative": 0, "neutral": 0, "totalCount": 0 },
        "TV": {"positive": 0, "negative": 0, "neutral": 0, "totalCount": 0 }}

def plot_graph(category,color):
    xCoordinates = []
    yCoordinates = []
    xLabels = []
    counter = 1
    
    for val in answerPercentages:
        xCoordinates.append(counter)
        yCoordinates.append(math.floor(answerPercentages[val][category]))
        xLabels.append(val)
        counter += 1

    fig, ax = plt.subplots()

    rects = ax.bar(xCoordinates, yCoordinates, 0.75, color=color)

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%d' % int(height),
                ha='center', va='bottom')

    
    ax.set_title(category)
    ax.set_xticks(xCoordinates)
    ax.set_xticklabels(xLabels)
    ax.set_xlabel('Category')
    ax.set_ylabel('% of comments')



    plt.savefig('%s.png' % category)


if __name__ == "__main__":
    
    
    
    with open(filepath, "r") as commentFile:
        commentReader = csv.reader(commentFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
        i = 0
        for row in commentReader:
            if i == 0:
                i=1
                continue
        
            (comment,label,category,prediction) = (row[0],row[1],row[2],row[3])

            if prediction == "positive":
                stats[category]["positive"] += 1
            elif prediction == "negative":
                stats[category]["negative"] += 1
            else:
                stats[category]["neutral"] += 1

            stats[category]["totalCount"] += 1

        for value in stats:
            positive = (stats[value]["positive"] / stats[value]["totalCount"]) * 100
            negative = (stats[value]["negative"] / stats[value]["totalCount"]) * 100
            neutral = (stats[value]["neutral"] / stats[value]["totalCount"]) * 100
            
            answerPercentages[value] = {"positive": positive,"negative": negative,"neutral": neutral}

        print(stats)
        print(answerPercentages)

        plot_graph("positive","green")
        plot_graph("negative","red")
        plot_graph("neutral","yellow")


