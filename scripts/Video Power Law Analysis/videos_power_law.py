import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # read data from csv
    temp_csv_2 = pd.read_csv("../../csv_files/video_data.csv",sep=",")
    video_len_draw = list(temp_csv_2["Length"])
    video_like_draw = list(temp_csv_2["Like"])
    video_view_draw = list(temp_csv_2["View"])

    video_len = [int(idx) for idx in video_len_draw]
    video_like = [int(idx) for idx in video_like_draw]
    video_view = [int(idx) for idx in video_view_draw]

    # like vs length
    liked_normalized = [0] * (max(video_like)//10+1)
    for idx in video_like:
      liked_normalized[idx//10] += 1

    xnew = []
    for idx in liked_normalized:
        xnew.append(idx/len(video_like))

    plt.figure(1)
    plt.ylim(0,500)
    plt.xlim(0,1000)
    plt.xlabel("Number of likes")
    plt.ylabel("Number of videos")
    plt.title("Frequency Distribution: Likes vs Videos")
    plt.text(600,450,r'x-axis:1 unit = 10 likes')
    plt.plot(liked_normalized)
    # plt.show()
    plt.savefig('graphs/plt1.png')

    plt.figure(2)
    plt.ylim(0,0.1)
    plt.xlim(0,100)
    plt.xlabel("Number of likes")
    plt.ylabel("Probability of videos")
    plt.title("Probability Distribution: Likes vs Videos")
    plt.text(60, 0.09, r'x-axis:1 unit = 10 likes')
    plt.plot(xnew)
    # plt.show()
    plt.savefig('graphs/plt2.png')

    # video length vs Number of views
    view_normalized = [0] * (max(video_len)//60+1)
    view_normalized_avg = [0] * (max(video_len)//60+1)

    for idx in range(len(video_len)):
        # if video_len[idx] >= 60:
        view_normalized[video_len[idx]//60] += video_view[idx]
        view_normalized_avg[video_len[idx]//60] += 1

    view_avg = view_normalized[:]
    for idx in range(len(view_normalized_avg)):
        if view_normalized_avg[idx] != 0:
            view_avg[idx] //= view_normalized_avg[idx]

    plt.figure(3)
    plt.xlim(0,180)
    plt.ylabel("Number of views")
    plt.xlabel("Length of videos")
    plt.title("Number of views vs Length of videos")
    plt.text(120,6500000000,r'x-axis:1 unit = 1 Min')
    plt.plot(view_normalized)
    # plt.show()
    plt.savefig('graphs/plt3.png')

    plt.figure(4)
    plt.xlim(0,180)
    plt.ylabel("Number of videos")
    plt.xlabel("Length of videos")
    plt.title("Number of videos vs Length of videos")
    plt.text(120,2300,r'x-axis:1 unit = 1 Min')
    plt.plot(view_normalized_avg)
    # plt.show()
    plt.savefig('graphs/plt4.png')

    plt.figure(5)
    plt.xlim(0,180)
    plt.ylabel("Average views")
    plt.xlabel("Length of videos")
    plt.title("Average views per video")
    plt.text(120,80000000,r'x-axis:1 unit = 1 Min')
    plt.plot(view_avg)
    # plt.show()
    plt.savefig('graphs/plt5.png')
